import uuid
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates/student")
router = APIRouter()
students_list = [
    {"id": "1", "name": "张三", "age": 20, "grade": "A"},
    {"id": "2", "name": "李四", "age": 22, "grade": "B"}
]


class StudentNew(BaseModel):
    id: str
    name: str
    age: int
    grade: str

@router.get('/student')
async def student_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"students": students_list})


@router.get("/add_student")
async def add_student_form(request: Request):
    return templates.TemplateResponse("add_student.html", {"request": request})


@router.post("/add_student")
async def add_student(request: Request):
    form_data = await request.form()
    new_student = StudentNew(id=str(uuid.uuid4()),**form_data)

    students_list.append(new_student.model_dump())
    return RedirectResponse(url="/student", status_code=303)


# 编辑学生
@router.get("/edit_student/{student_id}")
async def edit_student_form(request: Request, student_id: str):
    student = next((s for s in students_list if s["id"] == student_id), None)
    if student is None:
        return {"error": "Student not found"}
    return templates.TemplateResponse("edit_student.html", {"request": request, "student": student})


@router.post("/edit_student/{student_id}")
async def edit_student(request: Request):
    form_data = await request.form()
    print(form_data)
    # student = next((s for s in students_list if s["id"] == student_id), None)
    # if student is None:
    #     return {"error": "Student not found"}
    # student["name"] = name
    # student["age"] = age
    # student["grade"] = grade
    return RedirectResponse(url="/student", status_code=303)


# 删除学生
@router.get("/delete_student/{student_id}")
async def delete_student(student_id: str):
    global students_list
    students_list = [s for s in students_list if s["id"] != student_id]
    return RedirectResponse(url="/student", status_code=303)
