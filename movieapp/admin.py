from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.
admin.site.register(ImageCarosel)
admin.site.register(MoviesModel)
admin.site.register(Customer)
admin.site.register(Partner)



# Ticket
class MovieTicketsAdmin(admin.ModelAdmin):
    list_display = ("movie_name", "client_name", "phone_number", "cinema_hall", "seats", "payment_status", "view_ticket")
    search_fields = ("movie_name", "client_name", "phone_number")
    list_filter = ("payment_status", "cinema_hall")

    def view_ticket(self, obj):
        return format_html(f'<a href="/download-ticket/{obj.ticket_id}/" class="button">🎟 Download</a>')

    view_ticket.short_description = "Download Ticket"

admin.site.register(MovieTickets, MovieTicketsAdmin)