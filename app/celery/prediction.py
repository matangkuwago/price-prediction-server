import os
import gc
import gpt_2_simple as gpt2
import tensorflow as tf
import logging
from enum import Enum
from app.config import Config
from app.schemas import PredictionInput


class PriceMovement(str, Enum):
    INVALID = "-"
    SAME = "S-"
    UP = "U-"
    DOWN = "D-"


def get_checkpoints(folder_path='./checkpoint'):
    all_entries = os.listdir(folder_path)
    checkpoints = [name for name in all_entries if os.path.isdir(
        os.path.join(folder_path, name))]

    return checkpoints


def get_encoding(previous_value, current_value):
    if previous_value is None:
        return PriceMovement.INVALID

    if previous_value == current_value:
        return PriceMovement.SAME

    if current_value > previous_value:
        return PriceMovement.UP

    if previous_value > current_value:
        return PriceMovement.DOWN


def get_word_encoding(encoding: str):
    if encoding == PriceMovement.DOWN:
        return "down"

    if encoding == PriceMovement.UP:
        return "up"

    return ""


def encode_price_movement(prices: list[float]) -> str:
    price_iterator_a = iter(prices)
    price_iterator_b = iter(prices[1:])
    price_tuples = list(zip(price_iterator_a, price_iterator_b))
    encoded_price = "".join([get_encoding(x[0], x[1]) for x in price_tuples])
    return encoded_price


def _predict_raw(model: str, temperature: float, top_p: float, price_movement: str, length: int) -> str:
    logger = logging.getLogger(Config.LOGGER_NAME)
    logger.info(f"GPT temperature: {temperature}")
    logger.info(f"GPT top_p: {top_p}")
    logger.info(f"GPT model: {model}")
    logger.info(f"GPT output length: {length}")

    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name=model)
    result = gpt2.generate(sess,
                           run_name=model,
                           length=length,
                           temperature=temperature,
                           top_p=top_p,
                           prefix=price_movement,
                           return_as_list=True
                           )[0]
    tf.compat.v1.reset_default_graph()
    sess.close()
    gc.collect()
    return result


def predict(prediction_input: PredictionInput) -> list[str]:
    model = prediction_input.model
    temperature = prediction_input.temperature if prediction_input.temperature is not None else Config.GPT_TEMPERATURE
    top_p = prediction_input.top_p if prediction_input.top_p is not None else Config.GPT_TOP_P
    num_predictions = prediction_input.num_predictions
    encoded_price_movement = encode_price_movement(
        prediction_input.price_history)
    num_prefix = int(len(encoded_price_movement) / Config.CHAR_PER_PREDICTION)
    len_prefix = num_prefix * Config.CHAR_PER_PREDICTION
    len_prediction = num_predictions * Config.CHAR_PER_PREDICTION

    prediction_raw = _predict_raw(model,
                                  temperature,
                                  top_p,
                                  encoded_price_movement,
                                  len_prediction)

    prediction = prediction_raw[len_prefix:(len_prefix+len_prediction)]
    prediction_list = [get_word_encoding(prediction[i:i+2])
                       for i in range(0, len(prediction), 2)]

    logger = logging.getLogger(Config.LOGGER_NAME)
    logger.debug(f"num_input: {num_prefix}")
    logger.debug(f"encoded_price_movement: {encoded_price_movement}")
    logger.debug(f"prediction_raw: {prediction_raw}")
    logger.debug(f"prediction: {prediction}")
    logger.debug(f"prediction_list: {prediction_list}")

    return prediction_list
