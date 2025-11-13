# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import eea.api.visualizationutils


class EeaApiVisualizationutilsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=eea.api.visualizationutils)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "eea.api.visualizationutils:default")


EEA_API_VISUALIZATIONUTILS_FIXTURE = EeaApiVisualizationutilsLayer()


EEA_API_VISUALIZATIONUTILS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_API_VISUALIZATIONUTILS_FIXTURE,),
    name="EeaApiVisualizationutilsLayer:IntegrationTesting",
)


EEA_API_VISUALIZATIONUTILS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEA_API_VISUALIZATIONUTILS_FIXTURE,),
    name="EeaApiVisualizationutilsLayer:FunctionalTesting",
)
