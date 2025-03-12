from os.path import join, dirname, basename
from textwrap import dedent
from kivy.clock import triggered
from kivy.lang import Builder
from components.list.list import pre_compute_data
from features.basescreen import BaseScreen

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
