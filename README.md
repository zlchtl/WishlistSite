# Небольшой студенческий проект сайта с вишлистами на django

Его основная функция - создание и хранение индивидуальных вишлистов для каждого пользователя, а также отслеживание уже зарезервированных для покупки подарков.

```mermaid
graph TD;
subgraph  
  main(/)-->|login|login(/login/);
  main-->|register|register(/register/);
  main-->|logout|logout(/logout/);
  main-->|wishlists|wishlists(/str:username/);
  main-->|wishlist|wishlist(/wishlist/str:slug/);
  main-->|reservation|reservation(/reserved/str:wishlist_slug/str:gift_slug);
  main-->|check-username-email|check(/check-username-email/);
  main-->|admin|admin(/admin/);
end
```
