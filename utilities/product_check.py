from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Product
from schemas import ProductAvailabilityRequest

async def check_single_product_availability(
    request: ProductAvailabilityRequest,
    db: AsyncSession
):

    try:
        product_id = request.product_id
        country_code = request.country_code.strip().upper()
        required_quantity = request.required_quantity

        # Check if the country_code exists in the database
        country_check = await db.execute(
            select(Product.country_code).filter(Product.country_code == country_code)
        )
        valid_country_code = country_check.scalar_one_or_none()

        if not valid_country_code:
            return {
                "product_id": product_id,
                "country_code": country_code,
                "available_quantity": 0,
                "status": "Invalid",
                "message": f"Country code '{country_code}' does not exist in the database.",
            }

        # Query the product
        result = await db.execute(
            select(Product).filter(
                Product.product_id == product_id,
                Product.country_code == country_code,
            )
        )
        product = result.scalar_one_or_none()

        # If product is not found or if available_quantity == 0
        if not product or product.product_quantity_number == 0:
            return {
                "product_id": product_id,
                "country_code": country_code,
                "available_quantity": 0,
                "status": "Out of Stock",
                "message": "Product is out of stock.",
            }

        available_quantity = product.product_quantity_number

        # Prepare response based on available quantity
        if available_quantity < required_quantity:
            status, message = "Partial", "Only partial quantity available."
        else:
            status, message = "Available", "Product is available."

        return {
            "product_id": product_id,
            "country_code": country_code,
            "available_quantity": available_quantity,
            "status": status,
            "message": message,
        }

    except Exception as e:
        return {
            "product_id": request.product_id,
            "country_code": request.country_code,
            "available_quantity": 0,
            "status": "Error",
            "message": f"An unexpected error occurred: {str(e)}",
        }
