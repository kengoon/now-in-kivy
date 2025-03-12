from kivy.factory import Factory


def register_factory():
    r = Factory.register
    r("CoverImage", module="components.image")
    r("CustomLabel", module="components.label")
    r("RealRecycleView", module="components.scrollview")
    r("Divider", module="components.divider")
    r("Icon", module="components.label")
    r("IconButton", module="components.button")
    r("BackgroundColorBehavior", module="components.behaviors")
    r("AdaptiveBehavior", module="components.behaviors")
    r("StencilBehavior", module="components.behaviors")
    r("CustomButton", module="components.button")
    r("CustomCheckbox", module="components.checkbox")
    r("DialogScrim", module="components.scrim")
    r("CustomTextInput", module="components.textinput")
    r("CircularProgressIndicator", module="components.progressindicator")
    r("LinearProgressIndicator", module="components.progressindicator")
    r("BlogList", module="components.list")
