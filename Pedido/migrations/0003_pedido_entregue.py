from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedido', '0002_alter_itempedido_ponto'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='entregue',
            field=models.BooleanField(default=False),
        ),
    ]
