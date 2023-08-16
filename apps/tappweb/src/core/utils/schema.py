from pydantic import BaseModel
from pydantic.alias_generators import to_camel  # noqa

import constants


class CamelCaseModel(BaseModel):
    """
    A schemas for Camelcase.
    """

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class SuccessResponse(CamelCaseModel):
    """
    A schemas model success response.
    """
    message: str = constants.SUCCESS
