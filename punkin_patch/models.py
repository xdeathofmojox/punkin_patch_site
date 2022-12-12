from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class Character(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = user_directory_path, blank=True)

    def __str__(self):
        return self.name

class PatchTemplate(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    characters = models.ManyToManyField(Character)

    def __str__(self):
        return self.name

class PatchInstance(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(PatchTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Vote(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['characterID1', 'characterID2', 'instance'], name='No duplicate votes in patch instance')
        ]

    def validate_different_characters(self, c1, c2):
        if c1 == c2:
            raise ValidationError("{} is the same as {}".format(c1, c2))

    def validate_winner_exists(self, winner, c1, c2):
        if not (winner == c1 or winner == c2):
            raise ValidationError("Winner: {} is not {} or {}".format(winner, c1, c2))

    #TODO: This is a candidate for refactor. Probably a more efficient method of doing this
    def validate_characters_in_patch(self, characters, patch):
        charactersInPatch = [x for x in patch.characters.all()]
        for character in characters:
            if not character in charactersInPatch:
                raise ValidationError("Character: {} is not in Patch: {}".format(character, patch))

    def clean(self):
        self.validate_different_characters(self.characterID1, self.characterID2)
        self.validate_winner_exists(self.winningCharacterID, self.characterID1, self.characterID2)

        patch = PatchTemplate.objects.get(id=self.instance.template.id)
        self.validate_characters_in_patch([self.characterID1, self.characterID2], patch)

    characterID1 = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character1"
    )
    characterID2 = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character2"
    )
    winningCharacterID = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="winningCharacter"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instance = models.ForeignKey(PatchInstance, on_delete=models.CASCADE)