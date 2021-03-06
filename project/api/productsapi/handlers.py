from piston.handler import BaseHandler
from app.contacts.models import Contact
from app.stock.models import Product
from core import Core
from piston.utils import rc

class ProductsHandler(BaseHandler):
    model = Product
    fields = ('id', 'name', 'description', 'price_out', (
        'files', ('id', 'name', 'tags', ('editor', ('first_name', 'last_name')), 'date_created', 'date_edited', 'get_file')))

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", Product).filter(trashed=False)
        if id:
            try:
                return all.get(id=id)
            except Contact.DoesNotExist:
                return rc.NOT_FOUND
        else:
            all = ProductsHandler.filter_products(all, request.GET)

        return all

    @staticmethod
    def filter_products(products, filter):
        name_startswith = (filter.get('name_startsWith', False))
        if name_startswith:
            products = products.filter(name__icontains=name_startswith)

        return products