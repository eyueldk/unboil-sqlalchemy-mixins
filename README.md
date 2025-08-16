
# unboil-sqlalchemy-mixins

Reusable SQLAlchemy mixins to reduce boilerplate in your Python ORM models.

## Installation

```bash
pip install unboil-sqlalchemy-mixins
```

## Mixins



### IdentifiableMixin
Adds a string `id` primary key. Optionally, use a prefix:
```python
from unboil_sqlalchemy_mixins import IdentifiableMixin

class User(IdentifiableMixin, Base): ...
# With prefix:
class PrefixedUser(IdentifiableMixin.with_id_prefix("user_"), Base): ...
```

### TimestampedMixin
Adds `created_at` and `updated_at` fields (auto-managed):
```python
from unboil_sqlalchemy_mixins import TimestampedMixin
class Post(TimestampedMixin, Base): ...
```



### TenantOwnedMixin
Adds a required, indexed `tenant_id` column. Optionally, specify a foreign key:
```python
from unboil_sqlalchemy_mixins import TenantOwnedMixin

class Invoice(TenantOwnedMixin, Base): ...
# With foreign key:
class InvoiceWithFK(TenantOwnedMixin.with_tenant_fk("tenants.id"), Base): ...
```



### UserOwnedMixin
Adds a required, indexed `user_id` column. Optionally, specify a foreign key:
```python
from unboil_sqlalchemy_mixins import UserOwnedMixin

class Note(UserOwnedMixin, Base): ...
# With foreign key:
class NoteWithFK(UserOwnedMixin.with_user_fk("users.id"), Base): ...
```

---
MIT License