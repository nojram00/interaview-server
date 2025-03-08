#A MongoDB model for the student_activitys collection
from mdb_models.base import BaseMongoModel
from models.student import StudentSchema, Student
from pydantic import BaseModel
from typing import List
from pprint import pprint
class Activities(BaseModel):
    topic : str | None
    score : int
    items : int

class StudentActivitySchema(BaseModel):
    student_info: StudentSchema
    subject : str
    written_works : List[Activities]
    performance_tasks : List[Activities]
    exams : List[Activities]

class OutputStudentActivitySchema(BaseModel):
    student_id : str
    subject : str
    written_works : List[Activities]
    performance_tasks : List[Activities]
    exams : List[Activities]

class StudentActivity(BaseMongoModel):
    
    collection_name = 'student_activities' # Create a collection with this name in the database

    @classmethod
    def add_activity(cls, data : StudentActivitySchema):
        """
        Add a new activity to the student_activities collection.
        """

        pprint(data)
        student = Student.find_or_create(data.student_info)

        activity = cls.find({'student_id': student, 'subject': data.subject})

        payload = OutputStudentActivitySchema(
            student_id = student,
            subject = data.subject,
            written_works = data.written_works,
            performance_tasks = data.performance_tasks,
            exams = data.exams
        )

        print(payload.model_dump())

        if activity:
            result = cls().collection.update_one({'_id': activity['_id']}, {'$set': payload.model_dump()})
        else:
            result = cls.create(**payload.model_dump())
        
        if result:
            return True
        return False
    
    @classmethod
    def get_student_activity(cls, student_id : str):
        """
        Get the activities of a student by its id.
        """
        return cls.find({'student_id': student_id})
    
    @classmethod
    def find_by_student_id(cls, student_id : str):
        """
        Find a student by its id.
        """
        return cls().collection.find({'student_id': student_id})