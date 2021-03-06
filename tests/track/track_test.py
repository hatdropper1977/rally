from unittest import TestCase

from esrally.track import track


class TrackTests(TestCase):
    def test_finds_default_challenge(self):
        default_challenge = track.Challenge("default", description="default challenge", default=True)
        another_challenge = track.Challenge("other", description="non-default challenge", default=False)

        self.assertEqual(default_challenge,
                         track.Track(name="unittest",
                                     description="unittest track",
                                     challenges=[another_challenge, default_challenge])
                         .default_challenge)

    def test_default_challenge_none_if_no_challenges(self):
        self.assertIsNone(track.Track(name="unittest",
                                      description="unittest track",
                                      challenges=[])
                          .default_challenge)

    def test_finds_challenge_by_name(self):
        default_challenge = track.Challenge("default", description="default challenge", default=True)
        another_challenge = track.Challenge("other", description="non-default challenge", default=False)

        self.assertEqual(another_challenge,
                         track.Track(name="unittest",
                                     description="unittest track",
                                     challenges=[another_challenge, default_challenge])
                         .find_challenge_or_default("other"))

    def test_uses_default_challenge_if_no_name_given(self):
        default_challenge = track.Challenge("default", description="default challenge", default=True)
        another_challenge = track.Challenge("other", description="non-default challenge", default=False)

        self.assertEqual(default_challenge,
                         track.Track(name="unittest",
                                     description="unittest track",
                                     challenges=[another_challenge, default_challenge])
                         .find_challenge_or_default(""))

    def test_does_not_find_unknown_challenge(self):
        default_challenge = track.Challenge("default", description="default challenge", default=True)
        another_challenge = track.Challenge("other", description="non-default challenge", default=False)

        self.assertIsNone(track.Track(name="unittest",
                                      description="unittest track",
                                      challenges=[another_challenge, default_challenge])
                          .find_challenge_or_default("unknown-name"))


class IndexTests(TestCase):
    def test_matches_exactly(self):
        self.assertTrue(track.Index("test").matches("test"))
        self.assertFalse(track.Index("test").matches(" test"))

    def test_matches_if_no_pattern_is_defined(self):
        self.assertTrue(track.Index("test").matches(pattern=None))

    def test_matches_if_catch_all_pattern_is_defined(self):
        self.assertTrue(track.Index("test").matches(pattern="*"))
        self.assertTrue(track.Index("test").matches(pattern="_all"))

    def test_str(self):
        self.assertEqual("test", str(track.Index("test")))


class DocumentCorpusTests(TestCase):
    def test_do_not_filter(self):
        corpus = track.DocumentCorpus("test", documents=[
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=5, target_index="logs-01"),
            track.Documents(source_format="other", number_of_documents=6, target_index="logs-02"),
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=7, target_index="logs-03"),
            track.Documents(source_format=None, number_of_documents=8, target_index=None)
        ])

        filtered_corpus = corpus.filter()

        self.assertEqual(corpus.name, filtered_corpus.name)
        self.assertListEqual(corpus.documents, filtered_corpus.documents)

    def test_filter_documents_by_format(self):
        corpus = track.DocumentCorpus("test", documents=[
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=5, target_index="logs-01"),
            track.Documents(source_format="other", number_of_documents=6, target_index="logs-02"),
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=7, target_index="logs-03"),
            track.Documents(source_format=None, number_of_documents=8, target_index=None)
        ])

        filtered_corpus = corpus.filter(source_format=track.Documents.SOURCE_FORMAT_BULK)

        self.assertEqual("test", filtered_corpus.name)
        self.assertEqual(2, len(filtered_corpus.documents))
        self.assertEqual("logs-01", filtered_corpus.documents[0].target_index)
        self.assertEqual("logs-03", filtered_corpus.documents[1].target_index)

    def test_filter_documents_by_indices(self):
        corpus = track.DocumentCorpus("test", documents=[
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=5, target_index="logs-01"),
            track.Documents(source_format="other", number_of_documents=6, target_index="logs-02"),
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=7, target_index="logs-03"),
            track.Documents(source_format=None, number_of_documents=8, target_index=None)
        ])

        filtered_corpus = corpus.filter(target_indices=["logs-02"])

        self.assertEqual("test", filtered_corpus.name)
        self.assertEqual(1, len(filtered_corpus.documents))
        self.assertEqual("logs-02", filtered_corpus.documents[0].target_index)

    def test_filter_documents_by_format_and_indices(self):
        corpus = track.DocumentCorpus("test", documents=[
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=5, target_index="logs-01"),
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=6, target_index="logs-02"),
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=7, target_index="logs-03"),
            track.Documents(source_format=track.Documents.SOURCE_FORMAT_BULK, number_of_documents=8, target_index=None)
        ])

        filtered_corpus = corpus.filter(source_format=track.Documents.SOURCE_FORMAT_BULK, target_indices=["logs-01", "logs-02"])

        self.assertEqual("test", filtered_corpus.name)
        self.assertEqual(2, len(filtered_corpus.documents))
        self.assertEqual("logs-01", filtered_corpus.documents[0].target_index)
        self.assertEqual("logs-02", filtered_corpus.documents[1].target_index)
