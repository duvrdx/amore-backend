from django.core.mail import EmailMessage
from .models import Order, Cart
import amora.settings as settings

def send_mail(costumer_email: str, message_body: str):
  
  subject = '[Amore | E-Commerce] Novo Pedido Criado 💜'
  sender = settings.EMAIL_HOST_USER
  recipient = [costumer_email]

  # Create an instance of EmailMessage
  message = EmailMessage(
      subject,
      message_body,
      sender,
      recipient,
      reply_to=[sender],
  )

  message.send()
  
def get_resume(order: Order):
    order_resume = ''
  
    for item in order.items.all():
        order_resume += f'{item.product.name} - R$ {item.on_create_price}\n'
  
    order_resume += f'\nTotal: R$ {order.total}'
  
    return order_resume

def send_order_to_costumer(cart: Cart, order_resume: str):
  
    costumer_name = cart.costumer.first_name
    costumer_email = cart.costumer.email
  
    costumer_message = (
        f'Olá {costumer_name},\n\n'
        f'Seu pedido foi realizado com sucesso! 💜\n\n'
        f'Abaixo segue o resumo do pedido:\n\n'
        f'{order_resume}\n\n'
        f'Obrigado por comprar conosco! Em breve você receberá uma mensagem com as informações de entrega. 😊'
        f'Para mais informações, entre em contato no WhatsApp: {settings.WHATSAPP_NUMBER}'
    )
  
    send_mail(costumer_email, costumer_message)

def send_order_to_admin(cart: Cart, order_resume: str):
  
    admin_email = settings.EMAIL_HOST_USER
  
    costumer_name = cart.costumer.first_name
    costumer_email = cart.costumer.email
    costumer_phone = cart.costumer.phone
  
    message = (
        f'Novo pedido cadastrado!\n\n'
        f'Abaixo segue o resumo do pedido de {costumer_name} | {costumer_email} | {costumer_phone}:\n\n'
        f'{order_resume}'
    )
    send_mail(admin_email, message)