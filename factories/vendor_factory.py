import factory
from app.utils import db
from random import randint
from app.models.vendor import Vendor


fake_tel = ''.join([str(randint(1, n)) for n in range(1, 12)])

class VendorFactory(factory.alchemy.SQLAlchemyModelFactory):
	
	
	class Meta:
		model = Vendor
		sqlalchemy_session = db.session
		
	id = factory.Sequence(lambda n: n)
	name = factory.Faker('name')
	address = factory.Faker('address')
	tel = fake_tel
	contact_person = factory.Faker('name')