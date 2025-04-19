from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Product
from schemas import ProductStockResponse, ProductCreate, ProductAvailabilityRequest
from typing import List
from utilities.product_check import check_single_product_availability
import asyncio

router = APIRouter()

@router.post("/", response_model=ProductStockResponse)
async def add_product_info(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Endpoint to add a new product based on the country code.
    """
    try:
        # Check if the product already exists for the given country code
        result = await db.execute(
            select(Product).filter(
                Product.product_id == product.product_id,
                Product.country_code == product.country_code,
            )
        )
        existing_product = result.scalar_one_or_none()

        if existing_product:
            raise HTTPException(
                status_code=400,
                detail=f"Product with ID {product.product_id} already exists for country {product.country_code}."
            )

        # Create new product instance
        new_product = Product(
            product_id=product.product_id,
            country_code=product.country_code,
            product_quantity_number=product.product_quantity_number
        )

        # Add the new product to the database
        db.add(new_product)
        await db.commit()

        return ProductStockResponse(
            product_id=product.product_id,
            country_code=product.country_code,
            available_quantity=product.product_quantity_number,
            status="Available",
            message="Product added successfully."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/availability")
async def check_product_info(
    request: ProductAvailabilityRequest,
    db: AsyncSession = Depends(get_db),
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
            raise HTTPException(
                status_code=400,
                detail=f"Country code '{country_code}' does not exist in the database."
            )

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
                "message": "Product is out of stock."
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
        # Return internal server error with exception details
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post("/availability_async")
async def check_availability_async(
    requests: List[ProductAvailabilityRequest],
    db: AsyncSession = Depends(get_db)
    ):

    
    tasks = [check_single_product_availability(request, db) for request in requests]
    results = await asyncio.gather(*tasks)

    return results