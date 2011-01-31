from django.db import models
from core import Core

class PersistentManager(models.Manager):
    def get_query_set(self):
        return super(PersistentManager, self).get_query_set().filter(deleted=False)

    def inCompany(self):
        return super(PersistentManager, self).get_query_set().filter(deleted=False, company = Core.current_user().get_company())


"""
    def for_company(self, *args, **kwargs):
        
        if 'deleted' in kwargs:
            deleted = kwargs['deleted']
        else:
            deleted = False
        
        try:
            u = Core.current_user()
            
            if not u:
                HttpResponseRedirect("/accounts/")
      
            company = Core.current_user().company
                     
            if deleted == None:
                qs = self.get_query_set().filter(company = company)
            else:
                qs = self.get_query_set().filter(deleted = deleted, company = company) 

            return qs 
            
        except:
            print "INGEN"
            raise Http404
        
    def for_user(self, *args, **kwargs):
        u = Core.current_user()

        if not u:
            HttpResponseRedirect("/accounts/")
        
        permitted = []       
               
        try:
            qs = self.for_company(*args, **kwargs)
            for l in qs.all():
                if Core.current_user().has_perm('view', l):
                    permitted.append(l.id)
        except:   
            raise Http404
        
        qs = self.get_query_set().filter(id__in=permitted)
        
        return qs
"""