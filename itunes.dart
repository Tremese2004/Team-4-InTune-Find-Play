import 'dart:convert';

import 'package:http/http.dart' as http;

// A song found on Apple's free iTunes Search API (no account or API key).
class Track {
  final String previewUrl; // 30-second audio clip
  final String artworkUrl; // album cover, 600x600

  const Track(this.previewUrl, this.artworkUrl);
}

// Finds the iTunes track for a song. Returns null if Apple doesn't have it.
Future<Track?> findTrack(String title, String artist) async {
  // Lowercase letters and numbers only, so "heart pt.6" matches "heart pt. 6".
  String clean(Object? text) =>
      '$text'.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '');

  final wantTitle = clean(title);
  final wantArtist = clean(artist.split(RegExp('[,&]')).first);

  final response = await http.get(Uri.https('itunes.apple.com', '/search', {
    'term': '$title $artist',
    'media': 'music',
    'entity': 'song',
    'limit': '25',
  })).timeout(const Duration(seconds: 10));

  if (response.statusCode != 200) return null;

  // Keeps results by the same artist whose title starts with ours,
  // which skips covers, karaoke versions and type beats.
  final matches = (jsonDecode(response.body)['results'] as List)
      .where((r) =>
          r['previewUrl'] != null &&
          clean(r['artistName']).contains(wantArtist) &&
          clean(r['trackName']).startsWith(wantTitle))
      .toList();

  if (matches.isEmpty) return null;

  // Prefers the exact title over remixes and "(feat. ...)" versions.
  final best = matches.firstWhere(
    (r) => clean(r['trackName']) == wantTitle,
    orElse: () => matches.first,
  );

  return Track(
    best['previewUrl'] as String,
    '${best['artworkUrl100'] ?? ''}'.replaceFirst('100x100bb', '600x600bb'),
  );
}
