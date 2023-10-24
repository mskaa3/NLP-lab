## NLP lab 1

## Temat: Wykrywanie mowy nienawiści w mediach społecznościowych

Wraz z dynamicznym rozwojem mediów społecznościowych, gdzie anonimowość znacząco ułatwia swobodne wyrażanie myśli, coraz
większy odsetek publikowanych informacji i postów staje się nacechowany negatywnie i zawiera elementy agresji słownej
lub dyskryminacji. Obecnie spora część ludzkiego życia, szczególnie młodzieży, toczy się 'w sieci', zatem mowa
nienawiści stwarza realne zagrożenie dla zdrowia psychicznego i społecznego. W związku z tym konieczne jest
opracowywanie metod, które z dużą skutecznością zidentyfikują podobne zachowania i umożliwią platformom społecznościowym
na ich usunięcie, a także 'ukaranie' potencjalnie szkodliwych użytkowników. Aktualne metody analizy języka naturalnego i
sztucznej inteligencji pozwalają na klasyfikowanie tekstów i komentarzy pod kątem zawierania negatywnych treści na
podstawie między innymi zawartych słów oraz ich kontekstu. Aby zbudować narzędzie, które pozwoli na skuteczne
rozróżnienie tekstów 'nieszkodliwych' od tych zawierające szkodliwe treści, należy zgromadzić reprezentatywną próbkę
danych pochodzących z wybranych źródeł, które zobrazują występujący problem.

## Wykorzystane źródła

* Korpus wzorcowy i pełny:
    * [reddit.com](https://www.reddit.com/) - Platforma społecznościowa, gdzie użytkownicy wspólnie tworzą i dzielą się
      treściami. Ideą jest odnajdywanie interesujących informacji w Internecie i przedstawianie ich innym użytkownikom,
      a także komentowanie aktywności innych użytkowników. Aktualnie reddit posiada około 170 mln zarejestrowanych
      użytkowników. Strona ta jest podzielona na społeczności o nazwie subreddits, związane z różnymi zainteresowaniami,
      a każdy użytkownik ma możliwość założenia własnego subreddit. Zapewnia to szeroki zakres tematyczny tekstów a
      także róźnorodny przedział wiekowy czy grupę społeczną twórców, co będzie wpływać na styl wypowiedzi. Dodatkowo ze
      względu na charakterystykę serwisu zawiera on treści o charakterze informacyjnym jak i opinie i dyskusje, a
      dodatkowo posty będą zawierać słownictwo slangowe i potoczne. Ze względu na fakt, że jest to serwis
      angielskojęzyczny, koniecznym będzie odfiltrowanie postów w języku polskim.

    * [wykop.pl](https://wykop.pl/) - Polski odpowiednik anglojęzycznego portalu reddit działający na tej samej
      zasadzie.

    * [youtube.com](https://www.youtube.com/) - Amerykański portal zapewniający darmową możliwość udostępniania,
      edytowania, transmitowania na żywo oraz komentowania filmów. Dane z serwisu Youtube powinny mieć nieco inną
      specyfikę niż dwa poprzednie źródła, ze względu na fakt, że nie jest to platforma 'dyskusyjna', a posty
      użytkowników są w znacznej większości bezpośrednimi opiniami dotyczącymi danego contentu.

* Korpus pełny:
    * [wikipedia.org](https://pl.wikipedia.org/wiki/) - Encyklopedia internetowa obsługująca wiele języków i działająca
      na zasadzie otwartej treści. Edytować i dodawać nowe treści może każdy użytkownik, a treści są następnie
      weryfikowane przez grupę innych, sprawdzonych użytkowników. W języku polskim zawiera ona ponad 740 tysięcy haseł a
      korzystanie z niej jest całkowicie darmowe. Dzięki temu zawarte w niej teksty będą zawierały bogate słownictwo w
      bardzo szerokim zakresie tematycznym, a także bardziej poprawne kontrukcje gramatyczne i budowe zdań niż zwykłe
      serwisy społecznościowe, co z kolei pozwoli modelowi na lepsze wyuczenie się schematów języka.

[RAW DANE POBRANE ZE ŹRÓDEL](https://drive.google.com/drive/folders/1XNp3cTFvuWA6bxP8FMDoa3MIWyAAilvj?usp=sharing)
