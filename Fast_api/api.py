import os
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Any
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if Supabase credentials are set
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials are not set in environment variables. Please set SUPABASE_URL and SUPABASE_KEY.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI app
app = FastAPI(title="Patient Dashboard API", 
              description="API for retrieving patient data by age groups",
              version="1.0.0")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Patient Dashboard API. Use /docs to see available endpoints."}

@app.get("/patients/elders", response_model=List[Dict[str, Any]])
async def get_patients_over_90():
    """
    Get all patients with age over 90
    """
    try:
        response = supabase.table("Patient_interview") \
                          .select("*") \
                          .gte("Age", 90) \
                          .execute()
        
        if not response.data:
            return []
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patients: {str(e)}")

@app.get("/patients/LateSeniors", response_model=List[Dict[str, Any]])
async def get_patients_75_to_89():
    try:
        response = supabase.table("Patient_interview") \
                          .select("*") \
                          .gte("Age", 75) \
                          .lte("Age", 89) \
                          .execute()
        
        if not response.data:
            return []
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patients: {str(e)}")

@app.get("/patients/EarlySeniors", response_model=List[Dict[str, Any]])
async def get_patients_60_to_74():
    try:
        response = supabase.table("Patient_interview") \
                          .select("*") \
                          .gte("Age", 60) \
                          .lte("Age", 74) \
                          .execute()
        
        if not response.data:
            return []
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patients: {str(e)}")

@app.get("/patients/LateMiddleAge", response_model=List[Dict[str, Any]])
async def get_patients_45_to_59():
    try:
        response = supabase.table("Patient_interview") \
                          .select("*") \
                          .gte("Age", 45) \
                          .lte("Age", 59) \
                          .execute()
        
        if not response.data:
            return []
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patients: {str(e)}")
    
@app.get("/patients/EarlyMiddleAge", response_model=List[Dict[str, Any]])
async def get_patients_30_to_44():
    try:
        response = supabase.table("Patient_interview") \
                          .select("*") \
                          .gte("Age", 30) \
                          .lte("Age", 44) \
                          .execute()
        
        if not response.data:
            return []
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patients: {str(e)}")
    
@app.get("/patients/YoungAdults", response_model=List[Dict[str, Any]])
async def get_patients_30_to_44():
    try:
        response = supabase.table("Patient_interview") \
                          .select("*") \
                          .gte("Age", 18) \
                          .lte("Age", 29) \
                          .execute()
        
        if not response.data:
            return []
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patients: {str(e)}")

@app.get("/diabetes-types", response_model=List[str])
async def get_diabetes_types():
    """
    Get all unique diabetes types from the Patient_interview table.
    """
    try:
        # Fetch all records and process on the client side
        response = supabase.table("Patient_interview") \
                          .select("DiabetesType") \
                          .execute()
        
        if not response.data:
            return []
        
        # Extract unique diabetes types
        diabetes_types = set()
        for record in response.data:
            if record.get("DiabetesType") and record.get("DiabetesType").strip():
                diabetes_types.add(record.get("DiabetesType"))
        
        return sorted(list(diabetes_types))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving diabetes types: {str(e)}")
    
@app.get("/location-types", response_model=List[str])
async def get_location_types():
    """
    Get all unique location types from the Patient_interview table.
    """
    try:
        # Fetch all records and process on the client side
        response = supabase.table("Patient_interview") \
                          .select("Location") \
                          .execute()
        
        if not response.data:
            return []
        
        # Extract unique diabetes types
        location_types = set()
        for record in response.data:
            if record.get("Location") and record.get("Location").strip():
                location_types.add(record.get("Location"))
        
        return sorted(list(location_types))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving location types: {str(e)}")


@app.get("/patients/by-location-type/{location_type}", response_model=List[Dict[str, Any]])
async def get_patients_by_location_type(location_type: str):
    """
    Get all patients with a specific location type, the frontend will use this to filter patients
    by location type.
    """
    try:
        response = supabase.table("Patient_interview") \
                          .select("*") \
                          .eq("Location", location_type) \
                          .execute()
        
        if not response.data:
            return []
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patients: {str(e)}")
    
    
@app.get("/patients/by-diabetes-type/{diabetes_type}", response_model=List[Dict[str, Any]])
async def get_patients_by_diabetes_type(diabetes_type: str):
    """
    Get all patients with a specific diabetes type, the frontend will use this to filter patients
    by diabetes type.
    """
    try:
        response = supabase.table("Patient_interview") \
                          .select("*") \
                          .eq("DiabetesType", diabetes_type) \
                          .execute()
        
        if not response.data:
            return []
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving patients: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)