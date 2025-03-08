#A MongoDB model for the students collection
from mdb_models.base import BaseMongoModel
from pydantic import BaseModel

class StudentSchema(BaseModel):
    first_name : str
    last_name : str
    section : str | None

class Student(BaseMongoModel):
    
    collection_name = 'students' # Create a collection with this name in the database

    @classmethod
    def create_student(cls, data : StudentSchema):
        """
        Add a new student to the students collection.
        """
        return cls.create(**data.model_dump())
    
    @classmethod
    def find_student(cls, data : StudentSchema):
        """
        Find a student in the students collection.
        """
        return cls.find(data.model_dump())
    
    @classmethod
    def get_student_id(cls, data : StudentSchema):
        """
        Get the id of a student.
        """
        student = cls.find_student(data)
        if student:
            return student['_id']
        return None
    
    @classmethod
    def find_or_create(cls, data : StudentSchema):
        """
        Find or create a student in the students collection.

        Returns the id of a student.
        """
        student = cls.find_student(data)
        if student:
            return str(student["_id"])
        created = cls.create_student(data)
        return str(created)
    
    @classmethod
    def student_list(cls, page=1):
        """
        Get a list of students.
        """
        return cls.paginate(page=page, limit=10)
    
if __name__ == '__main__':
    from pprint import pprint
    result = Student.find_or_create(StudentSchema(first_name='John', last_name='Doe II', section='A'))
    pprint(result)