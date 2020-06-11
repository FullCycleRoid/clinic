# Generated by Django 3.0.6 on 2020-06-06 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psy_tests', '0006_auto_20200606_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[(1, 'one_answer'), (2, 'multi_answer'), (3, 'text_answer')], default='one_answer', max_length=1),
        ),
    ]
