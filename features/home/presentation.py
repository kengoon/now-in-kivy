from os.path import join, dirname, basename
from textwrap import dedent
from kivy.clock import triggered
from kivy.lang import Builder
from components.list.list import pre_compute_data
from features.basescreen import BaseScreen
from sjbillingclient.jclass.billing import BillingResponseCode, ProductType
from sjbillingclient.tools import BillingClient

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class HomeScreen(BaseScreen):
    @triggered(2)
    def on_enter(self):
        summary = dedent(
            """
            Breaking news: Burkina Faso has reclaimed its gold mines from a British company, reportedly the largest mining firm in Africa. Following the takeover, President Ibrahim Traore swiftly nationalized the mines. This move mirrors the actions of Gaddafi in Libya, which subsequently became one of the wealthiest countries globally.
            
            #iloveafrica #politics #Africa #IbrahimTraore #BurkinaFaso

            Credit: I Love Africa
            """
        ).strip()
        title = "Breaking news: Burkina Faso has reclaimed its gold mines from a British company"
        self.ids.rv.data = pre_compute_data(
            self,
            [
                dict(
                    title=title,
                    summary=summary,
                    date="Dec 14, 2023",
                    post_type="Doc",
                    image="https://qph.cf2.quoracdn.net/main-qimg-937c29101d303a1565257487e1fafaff",
                )
                for _ in range(10)
            ]
        )

    def buy_product(self):
        def on_acknowledge_purchase_response(billing_result):
            if billing_result.getResponseCode() == BillingResponseCode.OK:
                print(billing_result.getDebugMessage())
                self.toast(billing_result.getDebugMessage())

        def on_purchases_updated(billing_result, null, purchases):
            if billing_result.getResponseCode() == BillingResponseCode.OK and not null:
                for purchase in purchases:
                    client.acknowledge_purchase(
                        purchase_token=purchase.getPurchaseToken(),
                        on_acknowledge_purchase_response=on_acknowledge_purchase_response
                    )

        client = BillingClient(on_purchases_updated=on_purchases_updated)

        def on_product_details_response(billing_result, product_details_list):
            if billing_result.getResponseCode() == BillingResponseCode.OK:
                client.launch_billing_flow(product_details=product_details_list)

        def on_billing_setup_finished(billing_result):
            if billing_result.getResponseCode() == BillingResponseCode.OK:
                client.query_product_details_async(
                    product_type=ProductType.SUBS,
                    products_ids=["read_articles"],
                    on_product_details_response=on_product_details_response,
                )

        client.start_connection(
            on_billing_setup_finished=on_billing_setup_finished,
            on_billing_service_disconnected=lambda: print("disconnected")
        )
