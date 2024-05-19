import sys
from androguard.core.apk import APK
from loguru import logger


def get_intent_filters(apk, intent_type, intent_list):
    for elem_name in intent_list:
        intent_filters = apk.get_intent_filters(intent_type, elem_name)
        print(f"{intent_type}: {elem_name}")
        for key in intent_filters:
            print(f"\t{key}: {intent_filters[key]}")


def print_manifest(apk_file):
    try:
        a = APK(apk_file)
        package_name = a.get_package()
        print("Package Name:\n", package_name)

        main_activity = a.get_main_activity()
        print("Main Activity:\n", main_activity)

        activities = a.get_activities()
        print("List of Activities:")
        for activity in activities:
            print(activity)

        print("\nIntent Filters:")

        # Print intent filters for each activity
        get_intent_filters(a, 'activity', activities)
        # Print intent filters for each service
        services = a.get_services()
        get_intent_filters(a, 'service', services)
        # Print intent filters for each receiver
        receivers = a.get_receivers()
        get_intent_filters(a, 'receiver', receivers)
        # Print intent filters for each provider
        providers = a.get_providers()
        get_intent_filters(a, 'provider', providers)
        # Print intent filters for each activity_alias
        activity_aliases = a.get_activity_aliases()
        get_intent_filters(a, 'activity_alias', activity_aliases)

    except Exception as e:
        print("An error occurred:", e)


def main():
    # Disable logs
    logger.remove()

    if len(sys.argv) != 2:
        print("Something wrong with the command line argument")
        sys.exit(1)

    apk_file = sys.argv[1]
    print_manifest(apk_file)


if __name__ == "__main__":
    main()
