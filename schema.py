from pydantic import BaseModel

#  1 - Base
class ItemBase(BaseModel):
    title: str
    description: str 
    price: float

#  2 - Request    ตัวขาเข้า - รับข้อมูล ไปใช้กับ ORM | ตัวขาออก - ส่งข้อมูล แปลง ORM เป็น JSON ส่งออกไปยัง client
class ItemCreate(ItemBase):
    # ภายในจะมี logic การแปลงข้อมูลจาก Pydantic Model ไปเป็น ORM Model
    # เช่นการลดราคา มีการคำนวณราคาใหม่ก่อนไปใช้กับ ORM
    pass #ยังไม่มี logic อะไรแค่รับมาแล้วส่งไป

# 3 - Response   ตัวขาออก - ส่งข้อมูล แปลง ORM เป็น JSON ส่งออกไปยัง client
class ItemResponse(ItemBase):
    id: int  # ต้องมี id ด้วยเพราะ ORM Model มี id
    class Config:           # ตัว pydantic มีตัวช่วยในการแปลงข้อมูลจาก ORM Model ไปเป็น Pydentic Model 
        from_attributes = True     # (ซึ่งก็เป็น JSON ในการส่งไปยัง client แหละ) ซึ่งต้องกำหนด orm_mode เป็น True เพื่อให้ Pydantic รู้ว่าเราจะใช้ ORM Model
