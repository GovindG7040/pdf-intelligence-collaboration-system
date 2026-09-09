from app.services.ingest_service import IngestService


def main():

    print("=" * 50)
    print("Starting Knowledge Base Ingestion")
    print("=" * 50)

    ingest_service = IngestService()

    ingest_service.ingest()

    print("=" * 50)
    print("Knowledge Base Ingestion Finished")
    print("=" * 50)


if __name__ == "__main__":

    main()