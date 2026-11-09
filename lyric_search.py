import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const InTuneApp());
}

class InTuneApp extends StatelessWidget {
  const InTuneApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'InTune - Find & Play',
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF140D25),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF9562D5),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const LyricSearchPage(),
    );
  }
}

class Song {
  final String title;
  final String artist;
  final String album;
  final String year;
  final String artwork;
  final String songUrl;

  const Song({
    required this.title,
    required this.artist,
    this.album = '',
    this.year = '',
    this.artwork = '',
    this.songUrl = '',
  });

  factory Song.fromJson(Map<String, dynamic> json) {
    String read(List<String> keys) {
      for (final key in keys) {
        final value = json[key];
        if (value != null && value.toString().trim().isNotEmpty) {
          return value.toString();
        }
      }
      return '';
    }

    return Song(
      title: read(['title', 'trackName', 'name', 'track_name']),
      artist: read(['artist', 'artistName', 'artist_name']),
      album: read(['album', 'albumName', 'album_name']),
      year: read(['year', 'releaseYear', 'release_year']),
      artwork: read([
        'artwork',
        'cover',
        'coverUrl',
        'cover_url',
        'image',
        'imageUrl',
        'image_url',
      ]),
      songUrl: read(['url', 'trackUrl', 'track_url', 'permalink']),
    );
  }
}

class LyricSearchPage extends StatefulWidget {
  const LyricSearchPage({super.key});

  @override
  State<LyricSearchPage> createState() => _LyricSearchPageState();
}

class _LyricSearchPageState extends State<LyricSearchPage> {
  final TextEditingController searchController =
      TextEditingController();

  final FocusNode searchFocus = FocusNode();

  List<Song> searchResults = [];

  bool isLoading = false;
  bool hasSearched = false;
  String? errorMessage;

  static const Color backgroundColor = Color(0xFF140D25);
  static const Color cardColor = Color(0xFF291D3B);
  static const Color purpleColor = Color(0xFF9562D5);
  static const Color lightPurple = Color(0xFFB88CFF);

  // Replace this with an appropriate contact email.
  static const String contactEmail = 'Johnsean623@gmail.com';

  Future<void> searchLyrics() async {
    final query = searchController.text.trim();

    if (query.isEmpty) {
      setState(() {
        errorMessage = 'Please enter a lyric or phrase first.';
        searchResults = [];
        hasSearched = false;
      });
      return;
    }

    FocusScope.of(context).unfocus();

    setState(() {
      isLoading = true;
      hasSearched = true;
      errorMessage = null;
      searchResults = [];
    });

    try {
      final uri = Uri.https(
        'lrc.red',
        '/search.json',
        {
          'q': query,
          'in': 'lyrics',
        },
      );

      final response = await http.get(
        uri,
        headers: {
          'Accept': 'application/json',
          'X-Client-ID':
              'InTune/1.0 (contact: $contactEmail)',
        },
      ).timeout(const Duration(seconds: 25));

      if (response.statusCode != 200) {
        if (response.statusCode == 429) {
          throw Exception(
            'Too many searches. Please wait a little and try again.',
          );
        }

        throw Exception(
          'The lyrics service returned error '
          '${response.statusCode}. Please try again.',
        );
      }

      final decoded = jsonDecode(response.body);

      List<dynamic> hits = [];

      if (decoded is List) {
        hits = decoded;
      } else if (decoded is Map) {
        final possibleHits =
            decoded['hits'] ??
            decoded['results'] ??
            decoded['tracks'] ??
            decoded['data'];

        if (possibleHits is List) {
          hits = possibleHits;
        } else {
          throw Exception(
            'The lyrics service returned an unexpected response.',
          );
        }
      } else {
        throw Exception(
          'The lyrics service returned an unexpected response.',
        );
      }

      final songs = hits
          .whereType<Map>()
          .map((item) => Song.fromJson(
                Map<String, dynamic>.from(item),
              ))
          .where((song) =>
              song.title.isNotEmpty || song.artist.isNotEmpty)
          .toList();

      if (!mounted) return;

      setState(() {
        searchResults = songs;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        errorMessage = e.toString().replaceFirst(
          'Exception: ',
          '',
        );

        if (e.toString().contains('TimeoutException')) {
          errorMessage =
              'The search took too long. Check your connection and try again.';
        }
      });
    } finally {
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  void clearSearch() {
    searchController.clear();

    setState(() {
      searchResults = [];
      errorMessage = null;
      hasSearched = false;
    });

    searchFocus.requestFocus();
  }

  Future<void> openSong(Song song) async {
    if (song.songUrl.isEmpty) {
      showSongDetails(song);
      return;
    }

    final uri = Uri.tryParse(song.songUrl);

    if (uri == null ||
        (uri.scheme != 'https' && uri.scheme != 'http')) {
      showSongDetails(song);
      return;
    }

    try {
      final opened = await launchUrl(
        uri,
        mode: LaunchMode.externalApplication,
      );

      if (!opened && mounted) {
        showSongDetails(song);
      }
    } catch (_) {
      if (mounted) {
        showSongDetails(song);
      }
    }
  }

  void showSongDetails(Song song) {
    showModalBottomSheet(
      context: context,
      backgroundColor: cardColor,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(25),
        ),
      ),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.fromLTRB(24, 25, 24, 35),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: 45,
                  height: 5,
                  decoration: BoxDecoration(
                    color: Colors.white30,
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),
              const SizedBox(height: 25),
              Row(
                children: [
                  artworkWidget(song.artwork, 85),
                  const SizedBox(width: 18),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          song.title.isEmpty
                              ? 'Unknown Song'
                              : song.title,
                          style: const TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 7),
                        Text(
                          song.artist.isEmpty
                              ? 'Unknown Artist'
                              : song.artist,
                          style: const TextStyle(
                            color: Colors.white70,
                            fontSize: 15,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 25),
              if (song.album.isNotEmpty)
                detailRow('Album', song.album),
              if (song.year.isNotEmpty)
                detailRow('Year', song.year),
              const SizedBox(height: 15),
              if (song.songUrl.isNotEmpty)
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      Navigator.pop(context);
                      await openSong(song);
                    },
                    icon: const Icon(Icons.open_in_new),
                    label: const Text('Open Song'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: purpleColor,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.all(15),
                    ),
                  ),
                ),
            ],
          ),
        );
      },
    );
  }

  Widget detailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 75,
            child: Text(
              label,
              style: const TextStyle(color: Colors.white54),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(color: Colors.white),
            ),
          ),
        ],
      ),
    );
  }

  Widget artworkWidget(String artwork, double size) {
    final uri = Uri.tryParse(artwork);

    if (artwork.isNotEmpty &&
        uri != null &&
        (uri.scheme == 'https' || uri.scheme == 'http')) {
      return ClipRRect(
        borderRadius: BorderRadius.circular(12),
        child: Image.network(
          artwork,
          width: size,
          height: size,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) {
            return artworkPlaceholder(size);
          },
        ),
      );
    }

    return artworkPlaceholder(size);
  }

  Widget artworkPlaceholder(double size) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: const Color(0xFF704A9A),
        borderRadius: BorderRadius.circular(12),
      ),
      child: const Icon(
        Icons.music_note,
        color: Colors.white,
        size: 38,
      ),
    );
  }

  Widget buildSearchField() {
    return TextField(
      controller: searchController,
      focusNode: searchFocus,
      textInputAction: TextInputAction.search,
      onSubmitted: (_) => searchLyrics(),
      style: const TextStyle(
        color: Colors.white,
        fontSize: 16,
      ),
      decoration: InputDecoration(
        hintText: 'Enter a lyric or phrase...',
        hintStyle: const TextStyle(color: Colors.white54),
        prefixIcon: const Icon(
          Icons.search,
          color: lightPurple,
        ),
        suffixIcon: IconButton(
          onPressed: clearSearch,
          icon: const Icon(
            Icons.close,
            color: Colors.white54,
          ),
        ),
        filled: true,
        fillColor: cardColor,
        contentPadding: const EdgeInsets.all(18),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }

  Widget buildSearchButton() {
    return SizedBox(
      width: double.infinity,
      height: 55,
      child: ElevatedButton(
        onPressed: isLoading ? null : searchLyrics,
        style: ElevatedButton.styleFrom(
          backgroundColor: purpleColor,
          foregroundColor: Colors.white,
          disabledBackgroundColor: purpleColor.withOpacity(0.5),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
        child: isLoading
            ? const SizedBox(
                width: 23,
                height: 23,
                child: CircularProgressIndicator(
                  color: Colors.white,
                  strokeWidth: 2,
                ),
              )
            : const Text(
                'Search Lyrics',
                style: TextStyle(
                  fontSize: 17,
                  fontWeight: FontWeight.bold,
                ),
              ),
      ),
    );
  }

  Widget buildSongCard(Song song, int index) {
    return Container(
      margin: const EdgeInsets.only(bottom: 13),
      decoration: BoxDecoration(
        color: cardColor,
        borderRadius: BorderRadius.circular(15),
        border: Border.all(
          color: const Color(0xFF49365F),
        ),
      ),
      child: ListTile(
        onTap: () => openSong(song),
        contentPadding: const EdgeInsets.all(12),
        leading: artworkWidget(song.artwork, 55),
        title: Text(
          song.title.isEmpty ? 'Unknown Song' : song.title,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 6),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                song.artist.isEmpty
                    ? 'Unknown Artist'
                    : song.artist,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: Colors.white70),
              ),
              if (song.album.isNotEmpty) ...[
                const SizedBox(height: 4),
                Text(
                  song.album,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    color: Colors.white38,
                    fontSize: 12,
                  ),
                ),
              ],
            ],
          ),
        ),
        trailing: const Icon(
          Icons.chevron_right,
          color: lightPurple,
        ),
      ),
    );
  }

  Widget buildResults() {
    if (isLoading) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(color: lightPurple),
            SizedBox(height: 15),
            Text(
              'Searching for your song...',
              style: TextStyle(color: Colors.white70),
            ),
          ],
        ),
      );
    }

    if (errorMessage != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.error_outline,
                color: Colors.orangeAccent,
                size: 45,
              ),
              const SizedBox(height: 15),
              Text(
                errorMessage!,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.white70,
                  fontSize: 15,
                ),
              ),
              const SizedBox(height: 18),
              OutlinedButton.icon(
                onPressed: searchLyrics,
                icon: const Icon(Icons.refresh),
                label: const Text('Try Again'),
              ),
            ],
          ),
        ),
      );
    }

    if (searchResults.isEmpty && hasSearched) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.music_off,
              color: Colors.white38,
              size: 55,
            ),
            SizedBox(height: 15),
            Text(
              'No matching songs found.',
              style: TextStyle(
                color: Colors.white70,
                fontSize: 17,
              ),
            ),
            SizedBox(height: 8),
            Text(
              'Try a different lyric phrase.',
              style: TextStyle(color: Colors.white38),
            ),
          ],
        ),
      );
    }

    if (searchResults.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.music_note,
              color: Color(0xFF76559C),
              size: 65,
            ),
            SizedBox(height: 15),
            Text(
              'Your song discoveries start here.',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.white70,
                fontSize: 15,
              ),
            ),
            SizedBox(height: 8),
            Text(
              'Enter a lyric above to get started.',
              style: TextStyle(color: Colors.white38),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      itemCount: searchResults.length,
      itemBuilder: (context, index) {
        return buildSongCard(searchResults[index], index);
      },
    );
  }

  @override
  void dispose() {
    searchController.dispose();
    searchFocus.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: backgroundColor,
      appBar: AppBar(
        backgroundColor: const Color(0xFF201431),
        elevation: 0,
        title: const Row(
          children: [
            Icon(
              Icons.graphic_eq,
              color: lightPurple,
              size: 30,
            ),
            SizedBox(width: 10),
            Text(
              'InTune',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 24,
              ),
            ),
          ],
        ),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 15, 20, 10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Find the song.',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Remember a lyric? Let InTune find it.',
                style: TextStyle(
                  color: Colors.white70,
                  fontSize: 15,
                ),
              ),
              const SizedBox(height: 26),
              buildSearchField(),
              const SizedBox(height: 15),
              buildSearchButton(),
              const SizedBox(height: 28),
              Row(
                children: [
                  const Text(
                    'Search Results',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 21,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const Spacer(),
                  if (searchResults.isNotEmpty)
                    Text(
                      '${searchResults.length} found',
                      style: const TextStyle(
                        color: Colors.white54,
                        fontSize: 13,
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 15),
              Expanded(child: buildResults()),
              const SizedBox(height: 8),
              const Center(
                child: Text(
                  'InTune - Discover music through lyrics',
                  style: TextStyle(
                    color: Colors.white38,
                    fontSize: 11,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
