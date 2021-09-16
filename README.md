# Opis funkcjonalności

## Rejestrowanie nowych użytkowników:
![register_errors](https://user-images.githubusercontent.com/63907920/133578030-f68a7f81-3e33-4433-8db7-32d3f1ef1d67.JPG)

Po wpisaniu nazwy użytkownika, która jest już zajęta pojawia się prośba o wybranie innej nazwy. Podobnie, gdy powtórzone hasło bedzię się różnić od tego wpisanego wyżej pojawia się wiadomość mówiąca o tym, że oba pola muszą być sobie równe.

## Logowanie:
![login_page](https://user-images.githubusercontent.com/63907920/133578790-71c59fe9-26a6-4e50-af98-a7ed8635d3dc.JPG)

W celu wyświetlenia strony głównej należy być zalogowanym. Po wpisaniu loginu i hasła możemy zaznaczyć opcję "Remember me", dzięki której nie zostaniemy wylogowaniu ze strony po zamknięciu okna w przeglądarce. Jeśli nie posiadamy konta możemy przejść do strony z rejestrowaniem nowych użytkowników, a jeśli zapomnieliśmy hasła możemy poprosić o wysłanie na maila linku do zresetowania hasła. 

## Strona główna:
![index_page](https://user-images.githubusercontent.com/63907920/133579473-704a5511-fe72-4445-8235-d1e1dd480724.JPG)

Na stronie głównej możemy dodać nowy post oraz zobaczyć wszystkie posty nasze oraz użytkowników, których obserwujemy. W pasku nawigacyjnym na górze strony możemy przejść do sekcji "explore" (wszyscy użytkownicy lub wszystkie posty), sekcji "popular" (najpopularniejsze tagi lub posty), sekcji "messages" (gdy dostaniemy nową wiadomość pojawia się ikonka z liczbą nieprzeczytanych wiadomości) lub przejść do strony profilowej bądź wylogować się. 

## Explore:
![user_popup](https://user-images.githubusercontent.com/63907920/133582584-7a037751-f6e6-48ed-a8c8-3de325bc50f4.JPG)

W sekcji "explore" możemy wyszukać użytkownika po jego nazwie. Po najechaniu na nazwę użytkownika pojawia się okienko z informacjami na temat tego użytkownika. Jeśli klikniemy na nazwę użytkownika zostaniemy przeniesieni na stronę profilową. 

## Strona profilowa:
![profile_page](https://user-images.githubusercontent.com/63907920/133581030-4d5052ff-32f8-4af0-bbe3-e78119580923.JPG)

Na stronie profilowej użytkownika można zobaczyć wszystkie jego posty, zaobserwować go, wysłać prywatną wiadomość lub wyświetlić wszystkie komenatrze przez niego napisane. Jeśli jest to nasza strona profilowa to możemy tutaj edytować swój profil. Klikając w liczbę obserwatorów możemy zobaczyć, kto obserwuje danego użytkownika

## Obserwatorzy:
![followers](https://user-images.githubusercontent.com/63907920/133584394-4e794551-8a0f-4455-8140-98e30703e403.JPG)

## Wysyłanie wiadomości:
![send_message](https://user-images.githubusercontent.com/63907920/133581435-8405150c-2b0d-4e9c-a64e-c24a09364ea2.JPG)

## Wyświetlanie wiadomości:
![messages](https://user-images.githubusercontent.com/63907920/133581687-d63975b2-e810-47a7-93d4-84b4012cec1a.JPG)

## Popularne posty:
![popular_posts](https://user-images.githubusercontent.com/63907920/133582098-4f16a0dc-d3c6-41b6-bf61-2632a959624d.JPG)

Przeglądając najpopularniejsze posty możemy wybrać z jakiego okresu czasu mają one pochodzić. 

## Wyświetlanie posta:
![post_page](https://user-images.githubusercontent.com/63907920/133582178-808d54e1-7e23-48fe-905e-2be9936e9496.JPG)

Klikając w wybranego posta przechodzimy na jego stronę, gdzie możemy przeczytać napisane pod nim komentarze lub napisać swój własny. Możemy też polajkować dany post. Klikając w liczbę lajków przechodzimy do strony, na której możemy zobaczyć, kto polajkował wybrany post lub komentarz.

## Wyświetlanie lajków
![likes](https://user-images.githubusercontent.com/63907920/133584147-dcc7f4a5-f5aa-4758-976a-f397d689b304.JPG)


# Włączanie aplikacji
set FLASK_APP = microblog.py

set FLASK_ENV = development

flask run

http://127.0.0.1:5000/


# Migracje

(venv)$ flask db migrate -m "what you did"

(venv)$ flask db upgrade
