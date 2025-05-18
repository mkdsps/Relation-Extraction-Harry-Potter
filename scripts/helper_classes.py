from pydantic import BaseModel

class Entity(BaseModel):
  id: int
  text: str
  type: str
  token_start: int
  token_end: int

class Relation(BaseModel):
  type: str
  head_id: int
  tail_id: int 


class DataPoint(BaseModel):
  id: int
  entities: list[Entity]
  relations: list[Relation]
  annotation_confidence: float

class Output(BaseModel):
  data_points: list[DataPoint]