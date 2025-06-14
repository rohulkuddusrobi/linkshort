from django.core.management.base import BaseCommand
from django.utils import timezone
from shortener.models import ShortURL

class Command(BaseCommand):
    help = 'Clean up expired URLs from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete URLs that expired more than N days ago (default: 30)',
        )

    def handle(self, *args, **options):
        now = timezone.now()
        cutoff_date = now - timezone.timedelta(days=options['days'])
        
        # Find expired URLs
        expired_urls = ShortURL.objects.filter(
            expires_at__isnull=False,
            expires_at__lt=cutoff_date
        )
        
        count = expired_urls.count()
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} expired URLs that expired more than {options["days"]} days ago'
                )
            )
            if count > 0:
                self.stdout.write('\nURLs that would be deleted:')
                for url in expired_urls[:10]:  # Show first 10
                    self.stdout.write(f'  - {url.short_code} -> {url.original_url[:50]}... (expired: {url.expires_at})')
                if count > 10:
                    self.stdout.write(f'  ... and {count - 10} more')
        else:
            if count > 0:
                expired_urls.delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully deleted {count} expired URLs that expired more than {options["days"]} days ago'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('No expired URLs found to delete')
                )
        
        # Show statistics
        total_urls = ShortURL.objects.count()
        active_urls = ShortURL.objects.filter(
            expires_at__isnull=True
        ).count() + ShortURL.objects.filter(
            expires_at__gte=now
        ).count()
        
        self.stdout.write(f'\nDatabase Statistics:')
        self.stdout.write(f'  Total URLs: {total_urls}')
        self.stdout.write(f'  Active URLs: {active_urls}')
        self.stdout.write(f'  Expired URLs: {total_urls - active_urls}')
