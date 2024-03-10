from django.db import models
from django.core.validators import MinLengthValidator

class Author(models.Model): # you have to register the model in admin.py file to be shown in the web admin page
    first_name=models.CharField(max_length=100, default = None)
    last_name=models.CharField(max_length=50, default = None) # type: ignore
    email=models.EmailField(null=True, default = None)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")

class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return(self.caption)

class Post(models.Model):
    title=models.CharField(max_length=50)
    excerpt=models.CharField(max_length=50)
    image=models.ImageField(upload_to="photos", null=True)
    date=models.DateField(auto_now = True)# it updates it by default with current time and date 
    #we have to check the Date documentatiom
    slug=models.SlugField(unique = True)# by defaulu django make it index since it is slugfield which has always db_oindex = True also it has unique values
    content=models.TextField(validators =[MinLengthValidator(10)])# used for long textes like articles
    author=models.ForeignKey(Author, on_delete = models.SET_NULL, null = True, related_name = "posts" )# to choose on_delete SET_NULL you need to make null=True 
    tags = models.ManyToManyField(Tag)

    def __str__(self):
    
        return(f"{self.title} {self.author}")


class Comment(models.Model):
    user_name = models.CharField(max_length = 50)
    user_email = models.EmailField()
    text = models.TextField(max_length= 500)
    post = models.ForeignKey(Post, on_delete = models.CASCADE , related_name = "comments")# we use comments access this table via post with post.comments.all()

    def __str__(self):
    
        return(f"{self.user_name} {self.post.title}")





