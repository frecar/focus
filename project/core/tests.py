from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner
from core import load_initial_data, Core
from core.auth.permission.models import  Permission, Role
from core.auth.user.models import User
from core.auth.group.models import Group
from app.customers.models import Customer
from datetime import datetime, timedelta

class FocusTestSuiteRunner(DjangoTestSuiteRunner):
    """
    Made just to escape a single test that failed in DJANGO itself
    This is a small HACK because of django wanting us to use django-users, we will do no such thing!
    """

    def run_suite (self, suite, **kwargs):
        """
        - Adds initial data
        - Removes a certain test from the suite before running it
        """

        # Add initial data that since Django won't be added on tests automaticly
        for app in settings.INSTALLED_APPS:
            load_initial_data(app, test=True)

        # Remove a test that fails because of django only
        new_suites = []
        for test in suite._tests:
            if hasattr(test, 'id') and not test.id().endswith('test_shortcut_view'):
                new_suites.append(test)

        suite._tests = new_suites

        return super(FocusTestSuiteRunner, self).run_suite(suite, **kwargs)


class FocusTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.get_or_create(username="test")[0]
        self.user2 = User.objects.get_or_create(username="test2", company=self.user1.get_company())[0]
        self.user3 = User.objects.get_or_create(username="test3", company=self.user1.get_company())[0]

        Core.set_test_user(self.user3)

        self.customer1 = Customer.objects.get_or_create(name="Customer1", cid=1)[0]
        self.customer2 = Customer.objects.get_or_create(name="Customer2", cid=2)[0]

        self.group1 = Group.objects.get_or_create(name="group1")[0]
        self.group2 = Group.objects.get_or_create(name="group2")[0]

        self.role_admin = Role.objects.get_or_create(name="Admin")[0]
        self.role_member = Role.objects.get_or_create(name="Member")[0]

        cache.clear()


class PermissionsTesting(FocusTest):
    def testUserPerm(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.user1.grant_role("Member", self.customer1)
        self.user1.grant_role("Admin", self.customer1)
        self.role_member.grant_actions("DELETE")

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)

    def testGiveRoleOnClasses(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", Customer), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), False)

        self.user1.grant_role("Member", Customer)
        self.user1.grant_role("Admin", Customer)
        self.role_member.grant_actions("DELETE")

        self.assertEqual(self.user1.has_permission_to("EDIT", Customer), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), True)

    def testGiveRoleOnClassesToGroups(self):
        self.group1.add_member(self.user1)

        self.assertEqual(self.user1.has_permission_to("EDIT", Customer), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), False)

        self.group1.grant_role("Member", Customer)

        self.assertEqual(self.user1.has_permission_to("VIEW", Customer), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), False)

        self.group1.grant_role("Admin", Customer)

        self.assertEqual(self.user1.has_permission_to("EDIT", Customer), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), True)


    def testGivePermToClasses(self):
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
        self.user2.grant_permissions("CREATE", Customer)
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should now have this perm")

    def testGiveAllPermission(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.user1.grant_role("Member", self.customer1)
        self.user1.grant_role("Admin", self.customer1)
        self.role_admin.grant_actions("ALL")

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("ALL", self.customer1), True)

    def testGiveAllPermissionsToGroup(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.group1.grant_role("Member", self.customer1)
        self.group1.grant_role("Admin", self.customer1)
        self.role_admin.grant_actions("ALL")

        self.group1.add_member(self.user1)

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("ALL", self.customer1), True)

    """
    def testGiveNegativeAllPermission(self):
        #First do normal test, and give valid permission
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")

        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                     to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Then create negative (delete) grants
        self.user2.grant_permissions("ALL", Customer, from_time=datetime.today(), negative=True)

        #Now, the user should not have permission any longer
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
    """
    
    def testTimeLimitedGrants(self):
        #First test
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                     to_date=datetime.today() + timedelta(1))
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Second test
        self.assertEqual(self.user2.has_permission_to("EDIT", self.customer1), False,
                         "The user should not have this perm")
        self.user2.grant_permissions("EDIT", self.customer1,
                                     to_date=datetime.today() + timedelta(1))
        self.assertEqual(self.user2.has_permission_to("EDIT", self.customer1), True, "The user should have this perm")

        #Third test
        self.assertEqual(self.user2.has_permission_to("LIST", Customer), False, "The user should not have this perm")
        self.user2.grant_permissions("LIST", Customer,
                                     from_date=datetime.today() + timedelta(1))
        self.assertEqual(self.user2.has_permission_to("LIST", Customer), False, "The user should not have this perm ")
        self.user2.grant_permissions("LIST", Customer,
                                     to_date=datetime.today() + timedelta(1))
        self.assertEqual(self.user2.has_permission_to("LIST", Customer), True, "The user should have this perm")

    """
    def testNegativeGrants(self):
        #First do normal test, and give valid permission
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                     to_date=datetime.today() + timedelta(1))
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Then create negative (delete) grants
        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(), negative=True)

        #Now, the user should not have permission any longer
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")


    def testNegativeTimeLimitedGrants(self):
        #First, grants normally, then give negative time limited
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")

        self.user2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                     to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Then create negative (delete) grants, but from_date tomorrow
        self.user2.grant_permissions("CREATE", Customer, negative=True, from_date=datetime.today() + timedelta(1))

        #Then the user should still have permission
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should still have this perm")

        #But then we add negative permission, from today
        self.user2.grant_permissions("CREATE", Customer, negative=True, )

        #Now, the user should not have permission any longer
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm.")

        #Check if the user now has two negative permission
        self.assertEqual(Permission.objects.filter(user=self.user2, negative=True).count(), 2)
    """

    def testUserInGroupPermissionByRoles(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.group1.grant_role("Member", self.customer1)
        self.group1.grant_role("Admin", self.customer1)
        self.role_member.grant_actions("DELETE")

        self.group1.add_member(self.user1)

        #Check if user is added properly
        self.assertEqual(self.group1.members.all()[0], self.user1)

        #Check if group has access
        self.assertEqual(self.group1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.group1.has_permission_to("DELETE", self.customer1), True)

        #Check if user gain access by group
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)

    def testUserInGroupPermissionByRolesInheritance(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.group2.grant_role("Member", self.customer1)
        self.group2.grant_role("Admin", self.customer1)
        self.role_member.grant_actions("DELETE")

        self.group1.add_member(self.user1)

        #Check if user is added properly
        self.assertEqual(self.group1.members.all()[0], self.user1)

        self.group1.parent = self.group2
        self.group1.save()

        #Check if group has access

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)

    def testUserInGroupPermissionClasses(self):
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")
        self.group1.grant_permissions("CREATE", Customer)
        self.group1.add_member(self.user2)
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should now have this perm")

    def testUserInGroupPermissionManuallyTimeLimited(self):
        self.group2.add_member(self.user2)

        #First test
        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), False, "The user should not have this perm")

        self.group2.grant_permissions("CREATE", Customer, from_time=datetime.today(),
                                      to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("CREATE", Customer), True, "The user should have this perm")

        #Second test
        self.assertEqual(self.user2.has_permission_to("EDIT", self.customer1), False,
                         "The user should not have this perm")

        self.group2.grant_permissions("EDIT", self.customer1,
                                      to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("EDIT", self.customer1), True, "The user should have this perm")

        #Third test
        self.assertEqual(self.user2.has_permission_to("LIST", Customer), False, "The user should not have this perm")
        self.group2.grant_permissions("LIST", Customer,
                                      from_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("LIST", Customer), False, "The user should not have this perm ")

        self.group2.grant_permissions("LIST", Customer,
                                      to_date=datetime.today() + timedelta(1))

        self.assertEqual(self.user2.has_permission_to("LIST", Customer), True, "The user should have this perm")


    def testWhoHasPermissionToDoSomething(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.group2.grant_role("Admin", self.customer1)

        self.group2.add_member(self.user1)
        self.group2.add_member(self.user2)

        self.assertEqual(self.user1 in self.customer1.who_has_permission_to("VIEW"), True)
        self.assertEqual(self.user2 in self.customer1.who_has_permission_to("EDIT"), True)
        self.assertEqual(self.user2 in self.customer1.who_has_permission_to("VIEW"), True)


    def testGrantRoleByUrls(self):
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        self.client.get('/grant/role/Member/user/%s/customers/customer/%s/' % (self.user1.id, self.customer1.id))
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("VIEW", self.customer1), True)

        self.client.get('/grant/role/Admin/user/%s/customers/customer/%s/' % (self.user1.id, self.customer1.id))

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)


    def testGrantRoleByUrlsToGroups(self):
        c = self.client

        self.group1.add_member(self.user1)

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        c.get('/grant/role/Member/group/%s/customers/customer/%s/' % (self.group1.id, self.customer1.id))

        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("VIEW", self.customer1), True)

        c.get('/grant/role/Admin/group/%s/customers/customer/%s/' % (self.group1.id, self.customer1.id))

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)


    def testGrantPermissionByUrls(self):
        c = self.client

        #Give permission for objects
        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        c.get('/grant/permission/view/user/%s/customers/customer/%s/' % (self.user1.id, self.customer1.id))

        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("VIEW", self.customer1), True)

        c.get('/grant/permission/edit/user/%s/customers/customer/%s/' % (self.user1.id, self.customer1.id))
        c.get('/grant/permission/delete/user/%s/customers/customer/%s/' % (self.user1.id, self.customer1.id))

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)

        #Give permission for classes
        c.get('/grant/permission/delete/user/%s/customers/customer/%s/' % (self.user1.id, "any"))
        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), True)

    def testGrantPermissionByUrlsToGroups(self):
        c = self.client

        self.group1.add_member(self.user1)

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)

        c.get('/grant/permission/VIEW/group/%s/customers/customer/%s/' % (self.group1.id, self.customer1.id))

        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), False)
        self.assertEqual(self.user1.has_permission_to("VIEW", self.customer1), True)

        c.get('/grant/permission/edit/group/%s/customers/customer/%s/' % (self.group1.id, self.customer1.id))
        c.get('/grant/permission/DELETE/group/%s/customers/customer/%s/' % (self.group1.id, self.customer1.id))

        self.assertEqual(self.user1.has_permission_to("EDIT", self.customer1), True)
        self.assertEqual(self.user1.has_permission_to("DELETE", self.customer1), True)

        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), False)

        #Give a group, a permissionon a class
        c.get('/grant/permission/delete/group/%s/customers/customer/%s/' % (self.group1.id, "any"))
        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), True)

        #Give a group, a role on a class
        c.get('/grant/role/Admin/group/%s/customers/customer/%s/' % (self.group1.id, "any"))
        self.assertEqual(self.user1.has_permission_to("DELETE", Customer), True)

    def testPermittedObjects(self):
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("VIEW", Customer), False)

        self.user1.grant_role("Member", self.customer1)
        self.group1.add_member(self.user1)
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("VIEW", Customer), True)
        self.assertEqual(self.customer2 in self.user1.get_permitted_objects("VIEW", Customer), False)
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("EDIT", Customer), False)
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("DELETE", Customer), False)

        self.role_member.grant_actions("DELETE")
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("DELETE", Customer), True)
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("EDIT", Customer), False)

        self.user1.grant_role("Admin", self.customer1)
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("EDIT", Customer), True)

    def testPermittedObjectsByGroups(self):
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("VIEW", Customer), False)
        self.group1.add_member(self.user1)
        self.group1.grant_role("Member", self.customer1)
        self.assertEqual(self.customer1 in self.user1.get_permitted_objects("VIEW", Customer), True)