
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
class PrefixedUser(IdentifiableMixin, Base, id_prefix="user_"): ...
```

### TimestampedMixin
Adds `created_at` and `updated_at` fields (auto-managed):
```python
from unboil_sqlalchemy_mixins import TimestampedMixin
class Post(TimestampedMixin, Base): ...
```

### TenantScopedMixin
Adds a required, indexed `tenant_id` column for multi-tenant apps:
```python
from unboil_sqlalchemy_mixins import TenantScopedMixin
class Invoice(TenantScopedMixin, Base): ...
```

### UserOwnedMixin
Adds a required, indexed `user_id` column. Optionally, specify a foreign key:
```python
from unboil_sqlalchemy_mixins import UserOwnedMixin
class Note(UserOwnedMixin, Base): ...
class NoteWithFK(UserOwnedMixin, Base, user_fk="users.id"): ...
```

---
MIT License