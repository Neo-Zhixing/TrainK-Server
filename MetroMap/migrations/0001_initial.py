# Generated by Django 2.0.5 on 2018-05-22 14:33

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('attr', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positionX', models.DecimalField(decimal_places=2, max_digits=10)),
                ('positionY', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.DecimalField(decimal_places=2, default=1, max_digits=3)),
                ('shape', models.IntegerField(choices=[(0, 'Square'), (1, 'Triangle'), (2, 'Curve'), (3, 'Parallel'), (4, 'Straight')])),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='MetroMap.Node')),
                ('name', models.CharField(max_length=30)),
                ('level', models.IntegerField(choices=[(0, 'Minor'), (1, 'Major'), (2, 'Interchange'), (3, 'Intercity')])),
            ],
            bases=('MetroMap.node',),
        ),
        migrations.AddField(
            model_name='segment',
            name='fromNode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_origin_segment', to='MetroMap.Node'),
        ),
        migrations.AddField(
            model_name='segment',
            name='toNode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_destination_segment', to='MetroMap.Node'),
        ),
        migrations.AddField(
            model_name='line',
            name='segments',
            field=models.ManyToManyField(related_name='lines', to='MetroMap.Segment'),
        ),
    ]
