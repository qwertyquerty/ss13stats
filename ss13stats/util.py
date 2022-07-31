from flask import abort, make_response, jsonify

from sqlalchemy import func

def abort_with_msg(message: str, code: int) -> None:
    """
    For standard error throwing with messages and codes
    """
    abort(make_response(jsonify(msg=message), code))

