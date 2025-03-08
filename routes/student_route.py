from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.student_activity import StudentActivitySchema, StudentActivity
from models.student import Student, StudentSchema

router = APIRouter()

@router.get("/students-activity")
async def get_students():
    activities = StudentActivity.all()
    return [{ "id" : str(activity['_id']), **{ k : v  for k, v in activity.items() if k != "_id" } } for activity in activities.to_list()]

@router.get("/students-activity/{student_id}")
async def get_student_activity(student_id: str):
    activities = StudentActivity.find_by_student_id(student_id)
    return [{ "id" : str(activity['_id']), **{ k : v  for k, v in activity.items() if k != "_id" } } for activity in activities.to_list()]

@router.post("/students-activity")
async def add_student_activity(data: StudentActivitySchema):
    from pprint import pprint
    print("========================")
    pprint(data)
    print("========================")
    response = StudentActivity.add_activity(data)

    if response:
        return {"message": "Activity added successfully."}
    
    return {"message": "Failed to add activity."}

@router.get("/students")
async def get_students(page: int = 1):
    students = Student.student_list(page)
    total = Student.count()
    last_page = (total + 9) // 10

    data = [{ "id" : str(student['_id']), **{ k : v  for k, v in student.items() if k != "_id" } } for student in students.to_list()]
    return {
        "current_page": page,
        "last_page": last_page,
        "total": total,
        "data": data
    }

@router.post("/students")
async def add_student(data: StudentSchema):
    response = Student.create_student(data)

    if response:
        return {"message": "Student added successfully."}
    
    return {"message": "Failed to add student."}

@router.get("/students/id/{student_id}")
async def get_student(student_id: str):
    from pprint import pprint
    student = Student.find_by_id(student_id)
    if student is None:
        return JSONResponse(status_code=404, content={"message": "Student not found."})
    return { "id" : str(student['_id']), **{ k : v  for k, v in student.items() if k != "_id" } }

@router.post("/students/find")
async def find_student(data: StudentSchema):
    student = Student.find_student(data)
    if not student:
        return JSONResponse(status_code=404, content={"message": "Student not found."})
    return { "id" : str(student['_id']), **{ k : v  for k, v in student.items() if k != "_id" } }