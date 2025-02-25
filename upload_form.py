import imghdr
from flask.ext.wtf import Form
from wtforms import FileField, SubmitField, ValidationError

class UploadForm(Form):
    image_file = FileField('Image file')
    submit = SubmitField('Submit')

    def validate_image_file(self, field):
        if field.data.filename[-4:].lower() != '.jpg':
            raise ValidationError('Invalid file extension')
        if imghdr.what(field.data) != 'jpeg':
            raise ValidationError('Invalid image format')