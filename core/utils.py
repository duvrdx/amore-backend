from django.core.mail import EmailMultiAlternatives  # Use EmailMultiAlternatives for HTML emails
from .models import Order, Cart
from django.conf import settings  # Correct import for settings


def send_mail(subject: str, message_body: str, recipient_list: list[str], from_email=None, html_message=None):
    from_email = from_email or settings.EMAIL_HOST_USER
    message = EmailMultiAlternatives(subject, message_body, from_email, recipient_list)
    if html_message:
        message.attach_alternative(html_message, "text/html")  # Attach HTML version
    message.send()


def get_resume(order: Order) -> str:
    order_resume = "<ul>"
    for item in order.items.all():
        order_resume += f"<li>{item.product.name} - R$ {item.on_create_price} - {item.product.get_size_display()}</li>"
    order_resume += f"</ul><p><strong>Total:</strong> R$ {order.total}</p>"
    return order_resume


def send_order_to_customer(cart: Cart, order_resume: str) -> None:
    customer_name = cart.customer.first_name
    customer_email = cart.customer.email

    customer_message = (
        f"<p>Olá {customer_name},</p>"
        "<p>Seu pedido foi realizado com sucesso! </p>"
        "<p>Abaixo segue o resumo do pedido:</p>"
        f"{order_resume}"
        "<p>Obrigado por comprar conosco! Em breve você receberá uma mensagem com as informações de entrega. "
        f"Para mais informações, entre em contato no WhatsApp: {settings.WHATSAPP_NUMBER}</p>"
    )

    send_mail(
        subject="[Amore | E-Commerce] Seu pedido foi confirmado!",
        message_body=customer_message,
        recipient_list=[customer_email],
        html_message=customer_message,  # Send as HTML
    )


def send_order_to_admin(cart: Cart, order_resume: str) -> None:
    admin_message = (
        f"<p>Novo pedido cadastrado</p>",
        f"<strong>Cliente:</strong> {cart.customer.first_name} {cart.customer.last_name}",
        f"<strong>Contato:</strong> {cart.customer.email} | {cart.customer.phone}",
        f"<strong>Itens:</strong>",
        f"{order_resume}"
    )
    
    send_mail(
        subject="[Amore | E-Commerce] Novo Pedido Criado",
        message_body=f"Novo pedido cadastrado!\n\n{order_resume}",
        recipient_list=[settings.EMAIL_HOST_USER],
        html_message=f"Novo pedido cadastrado!\n\n{order_resume}"
    )