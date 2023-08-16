from fastapi import APIRouter, status
from httpx import AsyncClient

from config import settings

router = APIRouter()
client = AsyncClient(base_url=settings.STRAPI_BASE_URL)

headers = {"Authorization": f"Bearer {settings.STRAPI_API_TOKEN}"}


@router.get("/contact-us", status_code=status.HTTP_200_OK, description="contact us cms", name="Contact Us CMS")
async def get_contact_us_cms():
    """
    we can add
    contact-uses?fields[0]=phone_number&field[1]=email_&populate[image][fields][0]=name&populate[logo][fields][1]=url
    """

    response = await client.get(
        "/contact-uses?fields[0]=phone_number&fields[1]=email_&populate[image][fields][0]=name&populate[image][fields][1]=url",
        headers=headers,
    )
    return response.json()
