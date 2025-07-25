from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, List
from datetime import datetime

# --- Tag Models ---
class TagBase(BaseModel):
    name: str = Field(..., description="Tag name", max_length=255)

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Parameter Models ---
class ParameterBase(BaseModel):
    name: Optional[str] = Field(None, description="Parameter display name", max_length=255)
    key: str = Field(..., description="Parameter key", max_length=255)
    value: Optional[str] = Field(None, description="Parameter value")
    description: Optional[str] = Field(None, description="Parameter description", max_length=1000)
    is_secret: bool = Field(default=False, description="Whether this parameter contains sensitive information")

class ParameterCreate(ParameterBase):
    tags: Optional[List[str]] = Field(default=[], description="List of tag names to associate with the parameter")

class ParameterUpdate(BaseModel):
    name: Optional[str] = None
    key: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    is_secret: Optional[bool] = None
    tags: Optional[List[str]] = None

class Parameter(ParameterBase):
    id: str
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []

    # Use Pydantic v2 approach
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        extra='ignore'
    )
    
    def model_dump(self, **kwargs):
        """Override model_dump to ensure name field is always included"""
        data = super().model_dump(**kwargs)
        # Ensure name field is always present in the output
        if 'name' not in data:
            data['name'] = self.name
        return data

# --- Solution Models ---
class SolutionBase(BaseModel):
    name: str = Field(..., description="Solution name", max_length=255)
    description: Optional[str] = Field(None, description="Solution description", max_length=1000)

class SolutionCreate(SolutionBase):
    pass

class SolutionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Solution(SolutionBase):
    id: str
    created_at: datetime
    updated_at: datetime
    parameters: List[Parameter] = []
    parameter_count: Optional[int] = 0  # Add parameter count field

    class Config:
        from_attributes = True

# --- User Models ---
class UserBase(BaseModel):
    username: str = Field(..., max_length=255)

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    """User login request model"""
    username: str
    password: str

class User(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# --- Token Models ---
class Token(BaseModel):
    """JWT token response model"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """JWT token data model"""
    username: Optional[str] = None

# --- API Response Models ---
class APIResponse(BaseModel):
    """Standard API response model"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None

# --- Search and Filter Models ---
class ParameterFilter(BaseModel):
    """Filter parameters for searching"""
    solution_id: Optional[str] = None
    tags: Optional[List[str]] = None
    key_pattern: Optional[str] = None
    is_secret: Optional[bool] = None

class BulkParameterOperation(BaseModel):
    """Bulk operations on parameters"""
    parameter_ids: List[str]
    operation: str = Field(..., description="Operation type: 'delete', 'tag', 'untag'")
    tags: Optional[List[str]] = None 

# --- Container Service Models ---
class ContainerServiceBase(BaseModel):
    name: str = Field(..., description="Container service name", max_length=255)
    compute_pool: str = Field(..., description="Compute pool name", max_length=255)
    spec: Optional[str] = Field(None, description="Service specification (YAML)", max_length=10000)
    min_instances: Optional[int] = Field(1, description="Minimum number of instances")
    max_instances: Optional[int] = Field(1, description="Maximum number of instances")

class ContainerServiceCreate(ContainerServiceBase):
    pass

class ContainerServiceUpdate(BaseModel):
    spec: Optional[str] = None
    min_instances: Optional[int] = None
    max_instances: Optional[int] = None

class ContainerService(ContainerServiceBase):
    status: str = Field(..., description="Service status (RUNNING, SUSPENDED, etc.)")
    created_at: datetime
    updated_at: Optional[datetime] = None
    endpoint_url: Optional[str] = None
    dns_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class ContainerServiceOperation(BaseModel):
    operation: str = Field(..., description="Operation type: 'start', 'stop', 'suspend', 'resume'")

# --- Compute Pool Models ---
class ComputePool(BaseModel):
    name: str
    state: str
    min_nodes: int
    max_nodes: int
    instance_family: str
    created_at: datetime
    
    class Config:
        from_attributes = True 