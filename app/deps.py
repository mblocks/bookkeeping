# -*- coding: utf-8 -*-
from fastapi import Request
from app import schemas


def get_current_user(request: Request):
    # request from gateway
    return schemas.CurrentUser(id=request.headers.get('x-consumer-id'),  # nopep8
                               third=request.headers.get('x-consumer-third'),  # nopep8
                               third_user_id=request.headers.get('x-consumer-third-user-id'),  # nopep8
                               third_user_name=request.headers.get('x-consumer-third-user-name', '').encode("Latin-1").decode("utf-8")  # nopep8
                               )
