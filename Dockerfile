FROM postgres:18.1

# تنظیمات پیش‌فرض (مقادیر رمز از سکرت‌های رانفلر خوانده می‌شود)
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=angel-dbhsl_db

# پورت پیش‌فرض
EXPOSE 5432
