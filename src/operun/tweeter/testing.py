# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import operun.tweeter


class OperunTweeterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=operun.tweeter)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'operun.tweeter:default')


OPERUN_TWEETER_FIXTURE = OperunTweeterLayer()


OPERUN_TWEETER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(OPERUN_TWEETER_FIXTURE,),
    name='OperunTweeterLayer:IntegrationTesting'
)


OPERUN_TWEETER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(OPERUN_TWEETER_FIXTURE,),
    name='OperunTweeterLayer:FunctionalTesting'
)


OPERUN_TWEETER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        OPERUN_TWEETER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='OperunTweeterLayer:AcceptanceTesting'
)
