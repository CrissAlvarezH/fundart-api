from django.db import models
from django.utils.html import mark_safe


class Image(models.Model):
    image = models.ImageField(upload_to="images/img")
    thumbnail = models.ImageField(upload_to="images/thumbnail")
    prompt = models.CharField(max_length=5000)
    description = models.CharField(max_length=100)
    tags = models.ManyToManyField("images.ImageTag")

    def preview(self):
        path = f"""
            <div style="display: flex">
                <div style="padding: 0 10px 0 0">
                    <img src="{self.image.url}" width="150" /> 
                    <p>Image</p>
                </div>
                
                <div>
                    <img src="{self.thumbnail.url}" width="150" />
                    <p>Thumbnail</p>
                </div>
            </div>
        """
        return mark_safe(path)

    def preview_mini(self):
        path = f'<img src="{self.image.url}" width="50" />'
        return mark_safe(path)

    def prompt_short(self):
        if len(self.prompt) > 16:
            return self.prompt[0:15] + "..."
        return self.prompt

    def description_short(self):
        if len(self.description) > 15:
            return self.description[0:15] + "..."
        return self.description

    def tag_list(self):
        return [t.name for t in self.tags.all()]

    def __str__(self):
        return f"{self.id}: {self.description[0:15]}"


class ImageTag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class ImageFavorite(models.Model):
    image = models.ForeignKey("images.Image", on_delete=models.DO_NOTHING)
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def preview_mini(self):
        path = f'<img src="{self.image.image.url}" width="30" />'
        return mark_safe(path)

    def preview(self):
        path = f'<img src="{self.image.image.url}" width="150" />'
        return mark_safe(path)

    def __str__(self):
        return f"{self.user} - {self.image}"
