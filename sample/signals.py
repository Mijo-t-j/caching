from django.dispatch import receiver
from sample.models import (
    Matches
)
from django.db.models.signals import post_save, post_delete
from sample.services import MatchesService
from django.core.cache import caches, cache

@receiver(post_save, sender=Matches)
@receiver(post_delete, sender=Matches)
def invalidate_cache_on_matches_change(sender, instance, **kwargs):
    # Assuming your cache_endpoint_with_deleter decorator adds a
    # 'delete_cache' method to the wrapped view
    # Get the view function (e.g., List)
    view_func = getattr(MatchesService, 'List')
    print(f"view_func: {view_func}")

    cache_instance = caches['redis']
    # delete_pattern = cache_instance.clear()

    # print(f"delete_pattern: {delete_pattern}")
    # print(f"caches: {cache_instance.__dict__}")
    # Call the delete_cache method
    # view_func.delete_cache()

    # Access the raw Redis client
    redis_client = cache._cache.get_client()

    # Fetch all keys (use a pattern if needed)
    keys = redis_client.keys('*')  # Get all keys
    print(f"Keys: {keys}")


    # # Specify the key to delete
    # key_to_delete = b':1:views.decorators.cache.cache_page.match-list.GET.e55cdb22bca08af21a8f0eed48bae931.9cfefed8fb9497baa5cd519d7d2bb5d7.en-us.UTC'

    # # Delete the key
    # deleted_count = redis_client.delete(key_to_delete)
    # if deleted_count:
    #     print(f"Key {key_to_delete} deleted successfully!")
    # else:
    #     print(f"Key {key_to_delete} does not exist.")