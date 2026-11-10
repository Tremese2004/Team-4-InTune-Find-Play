
import 'itunes.dart';
import 'lyric_search_page.dart';
import 'song_detector_page.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/cupertino.dart' show CupertinoIcons;
import 'package:flutter/material.dart';

// This is the starting point of the InTune application.
void main() {
  runApp(const InTuneApp());
}

// This class creates the main application.
class InTuneApp extends StatelessWidget {
  const InTuneApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // Removes the debug banner from the top corner.
      debugShowCheckedModeBanner: false,

      // Sets the application name.
      title: 'InTune',

      // Sets the overall app theme and background colour.
      theme: ThemeData(
        brightness: Brightness.dark,
        // Uses iPhone behaviour everywhere: the San Francisco font on iOS,
        // bouncy scrolling and iOS-style gestures.
        platform: TargetPlatform.iOS,
        scaffoldBackgroundColor: Colors.black,
        colorScheme: const ColorScheme.dark(primary: accent, surface: surface),
        // Pop-up messages float above the tab bar instead of covering it.
        snackBarTheme: SnackBarThemeData(
          behavior: SnackBarBehavior.floating,
          backgroundColor: surfaceRaised,
          contentTextStyle: const TextStyle(color: Colors.white, fontSize: 15),
          insetPadding: const EdgeInsets.fromLTRB(16, 0, 16, 156),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
        ),
        useMaterial3: true,
      ),

      // Opens the Music Search screen when the app starts.
      home: const MusicSearchScreen(),
    );
  }
}

// This class creates the Music Search screen.
// StatefulWidget allows the screen to update when the user interacts with it.
class MusicSearchScreen extends StatefulWidget {
  const MusicSearchScreen({super.key});

  @override
  State<MusicSearchScreen> createState() =>
      _MusicSearchScreenState();
}

// This class stores the information and actions for the Music Search screen.
class _MusicSearchScreenState extends State<MusicSearchScreen> {

  // Controls and stores the text entered into the search bar.
  final TextEditingController searchController =
      TextEditingController();

  // These variables store the colours used throughout the app.
  final Color background = const Color(0xFF000000);
  final Color purple = const Color(0xFFB69AFF);
  final Color pink = const Color(0xFFB69AFF); // same as purple: one accent
  final Color cardBackground = const Color(0xFF1C1C1E);

  // Stores the message displayed after a search.
  String searchMessage = '';

  // Stores the song and artist shown in the mini-player.
  String currentSong = 'Blinding Lights';
  String currentArtist = 'The Weeknd';

  // Album cover shown in the mini-player (empty until a song loads).
  String currentArtwork = '';

  // Tracks whether the mini-player is playing or paused.
  bool isPlaying = false;

  // Lets us open favorites from library.
  bool showingFavorites = false;

  // Plays the audio for the mini-player.
  final AudioPlayer player = AudioPlayer();

  // Keeps track of which bottom navigation tab is selected.
  // 0 = Home, 1 = Library, 2 = Search, 3 = Playlist,
  // 4 = Lyric Search, 5 = Song Detector (Voice Search).
  int selectedTab = 2;
  int previousTab = 2;


  void goBack() {
    setState(() {
      selectedTab = previousTab;
      showingFavorites = false;
    });
  }

  final Set<String> followedArtists = {};

  //Add or remove a song from Favorites
  void toggleFavorite(Map<String, String> song) {
    setState(() {
      final exists = favoriteSongs.any(
        (item) => item['title'] == song['title'],
      );

      if (exists) {
        favoriteSongs.removeWhere(
          (item) => item['title'] == song['title'],
        );
      } else {
        favoriteSongs.add(
          Map<String, String>.from(song),
        );
      }
    });
  }

  //Check whether a song is a favorite
  bool isFavorite(Map<String, String> song) {
    return favoriteSongs.any(
      (item) => item['title'] == song['title'],
    );
  }

  //Favorite screen
  Widget buildFavoriteScreen() {
    return StatefulBuilder(
      builder: (context, updateFavorites) {
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Padding(
              padding: EdgeInsets.all(20),
              child: Text(
                'Favorites',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),

            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: TextField(
                decoration: InputDecoration(
                  hintText: 'Search favorites..',
                  prefixIcon: const Icon(Icons.search),
                  filled: true,
                  fillColor: cardBackground,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                    borderSide: BorderSide.none,
                  ),
                ),
                onChanged: (value) {
                  updateFavorites(() {});
                },
              ),
            ),

            const SizedBox(height: 15),

            Expanded(
              child: favoriteSongs.isEmpty
                  ? const Center(
                    child: Text('You have no favorite songs yet.'),
                  )
                : ListView.builder(
                  itemCount: favoriteSongs.length,
                  itemBuilder: (context, index) {
                    final song = favoriteSongs[index];

                    return ListTile(
                      leading: Icon(
                        Icons.music_note,
                        color: pink,
                      ),

                      title: Text(song['title'] ?? ''),
                      subtitle: Text(song['artist'] ?? ''),

                      onTap: () => playLibrarySong(song),

                      trailing: IconButton(
                        icon: const Icon(
                          Icons.favorite,
                          color: Colors.pink,
                        ),
                        onPressed: () {
                          toggleFavorite(song);
                          updateFavorites(() {});
                        },
                      ),
                    );
                  },
                ),
            ),
          ],
        );
      },
    );
  }

  Map<String, String>? selectedArtistSong;

  //Opens Artist Information for the selected song
  void openArtistInformation(Map<String, String> song) {
    setState(() {
      selectedArtistSong = song;
    });

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: background,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, updateArtist) {
            final artist = song['artist'] ?? 'Unknown Artist';
            final isFollowed = followedArtists.contains(artist);

            return SizedBox(
              height: 600,
              child: Padding(
                padding: const EdgeInsets.all(22),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: Container(
                        width: 45,
                        height: 5,
                        decoration: BoxDecoration(
                          color: Colors.white38,
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                    ),

                    const SizedBox(height: 25),

                    const Icon(
                      Icons.person,
                      size: 75,
                      color: Colors.white70,
                    ),

                    const SizedBox(height: 15),

                    Text(
                      artist,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 27,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 15),

                    Row(
                      children: [
                        Expanded(
                          child: ElevatedButton(
                            onPressed: () {
                              playLibrarySong(song);
                              Navigator.pop(context);
                            },
                            child: const Text('Play Music'),
                          ),
                        ),

                        const SizedBox(width: 10),

                        Expanded(
                          child: OutlinedButton(
                            onPressed: () {
                              setState(() {
                                if (isFollowed) {
                                  followedArtists.remove(artist);
                                } else {
                                  followedArtists.add(artist);
                                }
                              });

                              updateArtist(() {});
                            },
                            child: Text(
                              'Related Songs',
                              style: TextStyle(
                                fontSize: 21,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ),

                        const SizedBox(height: 10),

                        ListTile(
                          leading: Icon(
                              Icons.music_note,
                              color: pink,
                            ),
                            title: Text(
                              song['title'] ?? ''
                            ),
                            subtitle: Text(artist),
                            onTap: () {
                              playLibrarySong(song);
                              Navigator.pop(context);
                            },
                          ),
                          
                          const SizedBox(height: 15),
                          
                          const Text(
                            'About the Artists',
                            style: TextStyle(
                              fontSize: 21,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          
                          const SizedBox(height: 8),
                            Text(
                              'Explore music by $artist. '
                              'Discover songs and keep track of your favorite artists.',
                                style: const TextStyle(
                                  color: Colors.white70,
                                ),
                            ),
                          ]),
                        ],
                      ),
                    ),
                  );
                },
              );
            },
          );
        }

  //Sample song catalog
  final List<Map<String, String>> songCatalog = [
    {'title': 'SET IT OFF', 'artist': 'Offset', 'duration': '3.02'},
    {'title': 'Under the Sun', 'artist': 'Dreamville, J. Cole, DaBaby, Lute', 'duration': '3.59'},
    {'title': 'Bodies', 'artist': 'Offset & JID', 'duration': '3.25'},
    {'title': 'Surround Sound', 'artist': 'JID, 21 Savage, Baby Tate', 'duration': '3.49'},
    {'title': 'Like That', 'artist': 'Future, Metro Boomin', 'duration': '4.27'},
    {'title': 'BUTTERFLY EFFECT', 'artist': 'Travis Scott', 'duration': '3.11'},
    {'title': 'heart pt.6', 'artist': 'Kendrick Lamar', 'duration': '4.10'},
    {'title': 'Do for love', 'artist': '2Pac', 'duration': '4.46'},
    {'title': 'meet the grahams', 'artist': 'Kendrick Lamar', 'duration': '6.06'},
    {'title': "Can't Tell Me Nothing ", 'artist': 'Kanye West', 'duration': '4.31'},
    {'title': 'Have You Ever', 'artist': 'Brandy', 'duration': '4.05'},
  ];

  //Library and listening activity
  final List<Map<String, String >> librarySongs = [];
  final List<Map<String, String >> favoriteSongs = [];
  final List<Map<String, String >> recentSaves = [];
  final List<Map<String, String >> recentPlays = [];

  //Initial playlists
  final Map<String, List<Map<String, String>>> playlists = {
    'Shower Jamz': [],
    'Gym Set': [],
    'Work Mix': [],
  };

  String activePlaylist = 'Shower Jamz';

  @override
  void initState() {
    super.initState();

    // Keeps the play/pause icon in sync with the audio player.
    player.onPlayerStateChanged.listen((state) {
      if (mounted) {
        setState(() => isPlaying = state == PlayerState.playing);
      }
    });

    playlists['Shower Jamz'] = songCatalog
        .map((song) => Map<String, String>.from(song))
        .toList();
    
    playlists['Gym Set'] = [
      songCatalog[4],
      songCatalog[5],
      songCatalog[0]
    ].map((song) => Map<String, String>.from(song)).toList();

    playlists['Work Mix'] = [
      songCatalog[6],
      songCatalog[8],
      songCatalog[10]
    ].map((song) => Map<String, String>.from(song)).toList();
  }

  // This list stores the information for all nine music genres.
  // Each genre has a name, background colour, image, and height.
  final List<Map<String, dynamic>> genres = [
    {
      'name': 'Hip Hop',
      'color': const Color(0xFF55DCE0),
      'image': 'assets/images/hiphop.png',
      'height': 160.0,
    },
    {
      'name': 'R&B',
      'color': const Color(0xFFFF555B),
      'image': 'assets/images/rnb.png',
      'height': 190.0,

      //imaging positioning and size
      'imageAlignment': Alignment.bottomRight,
      'imageScale': 2.1,
    },
    {
      'name': 'Pop',
      'color': const Color(0xFFFF914D),
      'image': 'assets/images/pop.png',
      'height': 240.0,
    },
    {
      'name': 'Jazz',
      'color': const Color(0xFF78D957),
      'image': 'assets/images/jazz.png',
      'height': 85.0,

      //imaging positioning and size
      'imageAlignment': Alignment.topLeft,
      'imageScale': 1.35,
    },
    {
      'name': 'Rock',
      'color': const Color(0xFFB8FF70),
      'image': 'assets/images/rock.png',
      'height': 85.0,
    },
    {
      'name': 'Afro Beats',
      'color': const Color(0xFFFF3038),
      'image': 'assets/images/afro.png',
      'height': 200.0,

      //imaging positioning and size
      'imageAlignment': Alignment.bottomLeft,
      'imageScale': 1.0,
    },
    {
      'name': 'Hits',
      'color': const Color(0xFFFF59BB),
      'image': 'assets/images/hits.png',
      'height': 235.0,

      //imaging positioning and size
      'imageAlignment': Alignment.bottomCenter,
      'imageScale': 1.7,
    },
    {
      'name': 'Country',
      'color': const Color(0xFF997500),
      'image': 'assets/images/country.png',
      'height': 130.0,
    },
    {
      'name': 'Blues',
      'color': const Color(0xFF0753B5),
      'image': 'assets/images/blues.png',
      'height': 180.0,
    },
  ];

  // This function runs when the user presses the Search button.
  void searchMusic() {
    // Gets the text entered by the user and removes extra spaces.
    final query = searchController.text.trim();

    // setState updates the screen when information changes.
    setState(() {
      // Checks whether the search bar is empty.
      if (query.isEmpty) {
        searchMessage = 'Please enter a song or artist.';
      } else {
        // Displays the search term entered by the user.
        // This is a demonstration, not a real music search.
        searchMessage =
            'You searched for "$query". Connect a music service to find real results.';
      }
    });
  }

  // This function runs when the user taps a genre card.
  void selectGenre(String genre) {
    setState(() {
      // Places the selected genre into the search bar.
      searchController.text = genre;

      // Clears the previous search message.
      searchMessage = '';
    });
  }

  // This function clears the search bar when the X is pressed.
  void clearSearch() {
    setState(() {
      searchController.clear();
      searchMessage = '';
    });
  }

  // This function switches the mini-player between playing and paused.
  // If nothing is loaded yet, it starts the song shown in the mini-player.
  Future<void> togglePlay() async {
    switch (player.state) {
      case PlayerState.playing:
        await player.pause();
      case PlayerState.paused:
        await player.resume();
      default:
        await playLibrarySong({'title': currentSong, 'artist': currentArtist});
    }
  }

  // This function plays the next song in the catalog.
  void nextSong() {
    final index = songCatalog.indexWhere((s) => s['title'] == currentSong);
    playLibrarySong(songCatalog[(index + 1) % songCatalog.length]);
  }

  // This function updates the selected bottom navigation tab.
  void selectNavigation(int index) {
    setState(() {
      if (selectedTab  != index) {
        previousTab = selectedTab;
      }

      selectedTab = index;
      showingFavorites = false;
    });
  }

  //Plays songs and updates recent plays
  Future<void> playLibrarySong(Map<String, String> song) async {
    final title = song['title'] ?? 'Unknown Song';
    final artist = song['artist'] ?? 'Unknown Artist';

    setState(() {
      currentSong = title;
      currentArtist = artist;
      currentArtwork = '';

      recentPlays.removeWhere(
        (item) => item['title'] == song['title'],
      );

      recentPlays.insert(
        0,
        Map<String, String>.from(song),
      );

      if (recentPlays.length > 10) {
        recentPlays.removeLast();
      }
    });

    try {
      // Stops the old song right away while the new one loads.
      await player.stop();

      final track = await findTrack(title, artist);

      // Ignores this result if the user picked another song while it loaded.
      if (!mounted || currentSong != title) return;

      if (track == null) throw Exception('No preview found');
      setState(() => currentArtwork = track.artworkUrl);
      await player.play(UrlSource(track.previewUrl));
    } catch (_) {
      if (!mounted || currentSong != title) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('No audio preview available for $title')),
      );
    }
  }

  //Saves a song to the library and recent saves
  void saveSong(Map<String, String> song) {
    setState(() {
      if (!librarySongs.any(
        (item) => item['title'] == song['title'],
      )) {
        librarySongs.add(Map<String, String>.from(song));
      }

      recentSaves.removeWhere(
        (item) => item['title'] == song['title'],
      );

      recentSaves.insert(
        0,
        Map<String, String>.from(song),
      );

      if (recentSaves.length > 10) {
        recentSaves.removeLast();
      }
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Saved ${song['title']} to your library'),
      ),
    );
  }

  //Creates a new playlist
  void createPlaylist() {
    final controller = TextEditingController();

    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        backgroundColor: cardBackground,
        title: const Text('Create Playlist'),
        content: TextField(
          controller: controller,
          autofocus: true,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            hintText: 'Playlist name',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () {
              final name = controller.text.trim();

              if (name.isNotEmpty &&
                  !playlists.containsKey(name)) {
                setState(() {
                  playlists[name] = [];
                });

                Navigator.pop(dialogContext);

                setState(() {
                  selectedTab = 3;
                });
                }
            },
            child: const Text('Create'),
          ),
        ],
      ),
    );
  }

  //Opens Library screen
  Widget buildLibraryScreen() {
    return SingleChildScrollView(
      padding: EdgeInsets.fromLTRB(20, 20, 20, bottomInset),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Your Library',
            style: TextStyle(
              fontSize: 28,
              color: Colors.white,
            ),
          ),

          const SizedBox(height: 8),

          Text(
            'Your music, all in one place',
            style: TextStyle(color: Colors.white70),
          ),

          const SizedBox(height: 25),

          // Library shortcuts 
          Row(
            children: [
              Expanded(
                child: libraryCard(
                  'Recent Saves',
                  recentSaves.length,
                  Icons.bookmark,
                  () => showSongCollection(
                    'Recent Saves',
                    recentSaves,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: libraryCard(
                  'Recent Plays',
                  recentPlays.length,
                  Icons.history,
                  () => showSongCollection(
                    'Recent Plays',
                    recentPlays,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 12),

          Row(
            children: [
              Expanded(
                child: libraryCard(
                  'Favorites',
                  favoriteSongs.length,
                  Icons.favorite,
                  () => showSongCollection(
                    'Favorites',
                    favoriteSongs,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: libraryCard(
                  'Saved Songs',
                  librarySongs.length,
                  Icons.library_music,
                  () => showSongCollection(
                    'Saved Songs',
                    librarySongs,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 30),


          //Playlist Header
          Row(
            mainAxisAlignment:MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'My Playlists',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),

              IconButton(
                onPressed: createPlaylist,
                icon: Icon(
                  Icons.add_circle,
                  color: purple,
                  size: 30,
                ),
              ),
            ],
          ),

          const SizedBox(height: 10),

          ...playlists.keys.map((name) {
            return ListTile(
              contentPadding: EdgeInsets.zero,
              leading: CircleAvatar(
                backgroundColor: cardBackground,
                child: Icon(
                  Icons.queue_music,
                  color: pink,
                ),
              ),
              title: Text(name),
              subtitle: Text(
                '${playlists[name]!.length} songs'
              ),
              trailing: const Icon(
                Icons.arrow_forward_ios,
                size: 16,
              ),
              onTap: () {
                setState(() {
                  activePlaylist = name;
                  selectedTab = 3;
                });
              },
            );
          }),
        ],
      ),
    );
  }

  //Reusable Library Card
  Widget libraryCard(
    String title,
    int count,
    IconData icon,
    VoidCallback onTap,
  ) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: cardBackground,
          borderRadius: BorderRadius.circular(15),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: purple, size: 27),
            const SizedBox (height: 12),
            Text(
              title,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 5),
            Text(
              '$count songs',
              style: const TextStyle(
                fontSize: 12,
                color: Colors.white70,
              ),
            ),
          ]
        )
      ),
    );
  }

  //Displays a selected song collection.
  void showSongCollection(
    String title,
    List<Map<String, String>> songs,
  ) {
    // Implementation for displaying the song collection goes here.
    showModalBottomSheet(
      context: context,
      backgroundColor: background,
      builder: (context) {
        return SizedBox(
          height: 450,
          child: Column (
            children: [

              Padding(
                padding: const EdgeInsets.all(18),
                child: Row(
                  children: [
                    //return to the previous screen
                    IconButton(
                      icon:const Icon(
                        Icons.arrow_back,
                        color: Colors.white,
                      ),
                      onPressed: () {
                        Navigator.pop(context);
                      },
                    ),

                    const SizedBox(width: 10),

                    Expanded(
                      child: Text(
                        title,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 22,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              Expanded(
                child: songs.isEmpty
                    ? const Center(
                        child: Text('No songs yet.'),
                      )
                      : ListView.builder(
                          itemCount: songs.length,
                          itemBuilder:(context, index) {
                            final song = songs[index];
                            
                            return songTile(song);
                          },
                        ),
              ),
            ],
          ),
        );
      },
    );
  }

  //Reusable song row
  Widget songTile(Map<String, String> song) {
    return ListTile(
      leading: CircleAvatar(
        backgroundColor: cardBackground,
        child: Icon(
          Icons.music_note,
          color: pink,
        ),
      ),

      title: Text(song['title'] ?? ''),
      subtitle: Text(song['artist'] ?? ''),

      trailing: PopupMenuButton<String>(
        onSelected: (action) {
          if (action == 'Play') {
            playLibrarySong(song);
          } else if (action == 'Save') {
            saveSong(song);
          } else if (action == 'Favorite') {
            toggleFavorite(song);
          }
        },
        itemBuilder:(context) => const [
          PopupMenuItem(
            value: 'Play',
            child: Text('Play'),
          ),
          PopupMenuItem(
            value: 'Save',
            child: Text('Save to Library'),
          ),
          PopupMenuItem(
            value: 'Favorite',
            child: Text('Add to Favorites'),
          )
        ],
      ),

      onTap: () => playLibrarySong(song),
    );
  }

  //Playlist Screen
  Widget buildPlaylistScreen() {
    final songs = playlists[activePlaylist] ?? [];

    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Playlist content goes here
          Row(
            children: [
              const Expanded(
                child: Text(
                  'My Playlist',
                  style: TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),

              IconButton(
                onPressed: renamePlaylist,
                icon: Icon(Icons.add, color: pink),
              ),
            ],
          ),

          const SizedBox(height: 15),

          Text(
            activePlaylist,
            style: TextStyle(
              fontSize: 21,
              color: purple,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 6),

          Text(
            '${songs.length} tracks',
            style: const TextStyle(
              color: Colors.white70,
            ),
          ),

          const SizedBox(height: 20),

          Expanded(
            child: songs.isEmpty
                ? const Center(
                  child: Text('Add songs to this playlist'),
                )
              : ListView.builder(
                itemCount: songs.length,
                itemBuilder:(context, index) {
                  final song = songs[index];

                  return ListTile(
                    leading: Icon(
                      Icons.music_note,
                      color: pink,
                    ),

                    title: Text(song['title'] ?? ''),
                    subtitle: Text(song['artist'] ?? ''),

                    onTap: () => playLibrarySong(song),

                    trailing: IconButton(
                      icon: const Icon(
                        Icons.remove_circle_outline,
                        color: Colors.redAccent,
                      ),
                      onPressed: () {
                        setState(() {
                          songs.removeAt(index);
                        });
                      }
                    ),
                  );
                },
              ),

          ),
        ],
      ),
    );
  }

  // Renames the current playlist.
  void renamePlaylist() {
    final controller = TextEditingController(
      text: activePlaylist,
    );

    showDialog<String>(
      context: context,
      builder: (dialogcontext) => AlertDialog(
        title: const Text('Rename Playlist'),

        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            hintText: 'New playlist name',
          ),
        ),

        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogcontext),
            child: const Text('Cancel'),
          ),

          ElevatedButton(
            onPressed: () {
              final newName = controller.text.trim();

              if (newName.isNotEmpty &&
                 !playlists.containsKey(newName)) {
                setState(() {
                  playlists[newName] =
                      playlists.remove(activePlaylist)!;
                  activePlaylist = newName;
                });

                Navigator.pop(dialogcontext);
              }
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  //Add songs to the current playlist.
  void addSongsToPlaylists() {
    showModalBottomSheet(
      context: context,
      backgroundColor: background,
      isScrollControlled: true,

      builder: (context) {
        return SizedBox(
          height: 500,
          child: Column(
            children: [
              const Padding(
                padding: EdgeInsets.all(18),
                child: Text(
                  'Add Songs',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),

              Expanded(
                child: ListView.builder(
                  itemCount: songCatalog.length,

                  itemBuilder: (context, index) {
                    final song = songCatalog[index];

                    return ListTile(
                      title: Text(song['title']!),
                      subtitle: Text(song['artist']!),

                      trailing: IconButton(
                        icon: Icon(
                          Icons.add_circle,
                          color: purple,
                        ),

                        onPressed: () {
                          setState(() {
                            final playlist =
                                playlists[activePlaylist]!;
                            
                            if (!playlist.any(
                              (item) =>
                                  item['title'] == song['title'],
                            )) {
                              playlist.add(
                                Map<String, String>.from(song),
                              );
                            }
                          });
                        },
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
  

  // Disposes of the search controller when the screen is removed.
  // This helps prevent unnecessary memory use.
  @override
  void dispose() {
    searchController.dispose();
    player.dispose();
    super.dispose();
  }

  Widget buildSelectedScreen() {
    if (showingFavorites) {
      return Column(
        children: [
          ListTile(
            leading: IconButton(
              icon: const Icon(Icons.arrow_back),
              onPressed: () {
                setState(() {
                  showingFavorites = false;
                });
              },
            ),
            title: const Text('Favorites'),
          ),
          Expanded(
            child: buildFavoriteScreen(),
          ),
        ],
      );
    }

    switch (selectedTab) {
      case 0:
        return buildHomeScreen();
      
      case 1:
        return buildLibraryScreen();
      
      case 2:
        return buildSearchScreen();
      
      case 3:
        return buildPlaylistScreen();
      
      case 4:
        return LyricSearchPage(
          onBack: goBack,
        );

      case 5:
        return SongDetectorPage(
          bottomInset: bottomInset,
          currentSong: currentSong,
          isPlaying: isPlaying,
          onPlay: playLibrarySong,
          onTogglePlay: togglePlay,
        );

      default:
        return buildSearchScreen();
    }
  }

  // Opens the Search tab and runs the search typed on Home.
  void openSearch() {
    setState(() {
      selectedTab = 2;
      showingFavorites = false;
    });
    searchMusic();
  }

  Widget buildHomeScreen() {
    return SingleChildScrollView(
      padding: EdgeInsets.fromLTRB(20, 12, 20, bottomInset),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Greeting as an iOS large title, with the profile button.
          Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Good morning',
                      style: TextStyle(color: textSecondary, fontSize: 15),
                    ),
                    Text(
                      'User',
                      style: TextStyle(
                        fontSize: 34,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 0.4,
                      ),
                    ),
                  ],
                ),
              ),
              Glass(
                radius: 24,
                child: IconButton(
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Profile is coming soon'),
                      ),
                    );
                  },
                  tooltip: 'Profile',
                  icon: const Icon(
                    CupertinoIcons.person_fill,
                    size: 20,
                    color: Colors.white,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 20),

          // Search field. Pressing search on the keyboard opens the results.
          TextField(
            controller: searchController,
            textInputAction: TextInputAction.search,
            onSubmitted: (_) => openSearch(),
            style: const TextStyle(fontSize: 17),
            decoration: InputDecoration(
              hintText: 'Lyrics, song or artist',
              hintStyle: const TextStyle(color: textSecondary, fontSize: 17),
              prefixIcon: const Icon(
                CupertinoIcons.search,
                size: 20,
                color: textSecondary,
              ),
              filled: true,
              fillColor: surface,
              contentPadding: const EdgeInsets.symmetric(vertical: 12),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(24),
                borderSide: BorderSide.none,
              ),
            ),
          ),

          const SizedBox(height: 24),

          // The two ways to find a song, as one grouped list.
          Material(
            color: surface,
            borderRadius: BorderRadius.circular(24),
            clipBehavior: Clip.antiAlias,
            child: Column(
              children: [
                entryRow(
                  icon: CupertinoIcons.mic_fill,
                  title: 'Voice Search',
                  subtitle: 'Hum or sing a song',
                  primary: true,
                  onTap: () => selectNavigation(5),
                ),
                const Divider(
                  height: 1,
                  thickness: 0.5,
                  indent: 68,
                  color: hairline,
                ),
                entryRow(
                  icon: CupertinoIcons.keyboard,
                  title: 'Type Lyrics',
                  subtitle: 'Know some of the words?',
                  onTap: () => selectNavigation(4),
                ),
              ],
            ),
          ),

          const SizedBox(height: 32),

          const Text(
            'Quick access',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 22,
              letterSpacing: 0.35,
            ),
          ),

          const SizedBox(height: 16),

          Row(
            children: [
              homeQuickButton(
                CupertinoIcons.music_note_list,
                'Your Playlist',
                () => selectNavigation(3),
              ),
              homeQuickButton(
                CupertinoIcons.heart_fill,
                'Favorites',
                () {
                  setState(() {
                    selectedTab = 1;
                    showingFavorites = true;
                  });
                },
              ),
              homeQuickButton(
                CupertinoIcons.clock_fill,
                'Search History',
                () => selectNavigation(1),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // One row in the Home list that opens Voice Search or Type Lyrics.
  // The primary one gets the accent color on its icon.
  Widget entryRow({
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
    bool primary = false,
  }) {
    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Row(
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: primary ? accent : surfaceRaised,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(
                icon,
                size: 20,
                color: primary ? onAccent : Colors.white,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w600,
                      letterSpacing: -0.4,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    subtitle,
                    style: const TextStyle(color: textSecondary, fontSize: 15),
                  ),
                ],
              ),
            ),
            const Icon(
              CupertinoIcons.chevron_forward,
              size: 16,
              color: Color(0x4DEBEBF5),
            ),
          ],
        ),
      ),
    );
  }

  Widget homeQuickButton(
    IconData icon,
    String title,
    VoidCallback onTap,
  ) {
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 8),
          child: Column(
            children: [
              Container(
                width: 56,
                height: 56,
                decoration: const BoxDecoration(
                  color: surface,
                  shape: BoxShape.circle,
                ),
                child: Icon(icon, size: 24, color: accent),
              ),
              const SizedBox(height: 8),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(color: textSecondary, fontSize: 13),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget buildSearchScreen() {
    return SingleChildScrollView(
      padding: EdgeInsets.only(bottom: bottomInset),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Search screen content goes here.
          SingleChildScrollView(
                // Adds spacing around the screen content.
                padding: const EdgeInsets.all(22),

                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [

                    // HEADER
                    // Displays the InTune logo and profile icon.
                    Row(
                      mainAxisAlignment:
                          MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            // Music equalizer icon.
                            Icon(
                              Icons.graphic_eq,
                              color: purple,
                              size: 42,
                            ),

                            const SizedBox(width: 10),

                            // InTune application name.
                            Text(
                              'InTune',
                              style: TextStyle(
                                color: purple,
                                fontSize: 34,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),

                        // Profile icon on the right side of the header.
                        IconButton(
                          onPressed: () {
                            ScaffoldMessenger.of(context)
                                .showSnackBar(
                              const SnackBar(
                                content: Text(
                                  'Profile screen coming soon!',
                                ),
                              ),
                            );
                          },
                          icon: const Icon(
                            Icons.account_circle_outlined,
                            size: 34,
                            color: Colors.white,
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 34),

                    // PAGE TITLE
                    // Introduces the Music Search screen.
                    const Text(
                      'Search Music',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 12),

                    // Short description underneath the page title.
                    const Text(
                      'Find your favorite songs, artists, and genres.',
                      style: TextStyle(
                        color: Color(0xFFB8B3C9),
                        fontSize: 16,
                      ),
                    ),

                    const SizedBox(height: 28),

                    // SEARCH FIELD
                    // Allows users to type a song or artist name.
                    TextField(
                      controller: searchController,

                      // Sets the colour and size of the typed text.
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 17,
                      ),

                      // Allows users to search by pressing Enter.
                      onSubmitted: (_) => searchMusic(),

                      decoration: InputDecoration(
                        // Text displayed before the user types.
                        hintText: 'Search songs or artists...',
                        hintStyle: const TextStyle(
                          color: Color(0xFFB8B3C9),
                        ),

                        // Search icon on the left side of the field.
                        prefixIcon: Icon(
                          Icons.search,
                          color: purple,
                          size: 29,
                        ),

                        // X button on the right clears the search.
                        suffixIcon: IconButton(
                          onPressed: clearSearch,
                          icon: const Icon(
                            Icons.close,
                            color: Color(0xFFB8B3C9),
                          ),
                        ),

                        // Gives the search field its dark background.
                        filled: true,
                        fillColor: cardBackground,

                        // Border shown when the search field is not selected.
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(25),
                          borderSide: BorderSide(
                            color: purple.withValues(alpha: 0.5),
                            width: 1.5,
                          ),
                        ),

                        // Border shown when the user selects the search field.
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(25),
                          borderSide: BorderSide(
                            color: purple,
                            width: 2,
                          ),
                        ),

                        // Adds space inside the search field.
                        contentPadding:
                            const EdgeInsets.symmetric(
                          vertical: 21,
                          horizontal: 18,
                        ),
                      ),
                    ),

                    const SizedBox(height: 16),

                    // SEARCH BUTTON
                    // Runs the searchMusic function when tapped.
                    SizedBox(
                      width: double.infinity,
                      height: 53,
                      child: ElevatedButton.icon(
                        onPressed: searchMusic,

                        // Search icon displayed inside the button.
                        icon: const Icon(
                          Icons.search,
                          color: Color(0xFF171323),
                        ),

                        // Text displayed inside the button.
                        label: const Text(
                          'Search',
                          style: TextStyle(
                            color: Color(0xFF171323),
                            fontSize: 17,
                          ),
                        ),

                        // Styles the button with the pink colour and rounded edges.
                        style: ElevatedButton.styleFrom(
                          backgroundColor: pink,
                          shape: RoundedRectangleBorder(
                            borderRadius:
                              BorderRadius.circular(30),
                          ),
                        ),
                      ),
                    ),

                    // SEARCH MESSAGE
                    // Only appears when a search message exists.
                    if (searchMessage.isNotEmpty) ...[
                      const SizedBox(height: 16),

                      Text(
                        searchMessage,
                        style: const TextStyle(
                          color: Color(0xFFB8B3C9),
                          fontSize: 15,
                        ),
                      ),
                    ],

                    const SizedBox(height: 38),

                    // GENRE SECTION TITLE
                    const Text(
                      'Browse Genres',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 20),

                    // GENRE CARDS
                    // This Row creates two cloumns of genre cards.
                    // Each colummn contains cards with different heights.
                    // creates the staggered layout shwin in the Canva design.
                    // GridView.builder creates all nine genre cards.

                    Row(
                      //Aligns both columns at the top
                      crossAxisAlignment: CrossAxisAlignment.start,

                      children: [

                        // LEFT COLUMN
                        // Expanded gives the left column half of the available width.
                        Expanded( 
                          child: Column(
                            children: [

                              //Displays the hiphop card
                              genreCard(genres[0]),

                              const SizedBox(height: 10),

                              //Displays the pop card
                              genreCard(genres[2]),

                              const SizedBox(height: 10),

                              //Displays the rock card
                              genreCard(genres[4]),

                              const SizedBox(height: 10),

                              //Displays the hits card
                              genreCard(genres[6]),
                            ],
                          ),
                        ),
                        // Adds apace between the two columns
                        const SizedBox(width: 10),

                        // RIGHT COLUMN
                        // Expanded gives the right column the remaining width.
                        Expanded(
                          child: Column(
                            children: [

                              //Displays the rnb card
                              genreCard(genres[1]),
                              
                              const SizedBox(height: 10),

                              //Displays the jazz card
                              genreCard(genres[3]),

                              const SizedBox(height: 10),

                              //Displays the afrobeat card
                              genreCard(genres[5]),

                              const SizedBox(height: 10),

                              //Displays the country card
                              genreCard(genres[7]),

                              const SizedBox(height: 10),

                              //Displays the blues card
                              genreCard(genres[8]),
                          ],
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      );
   }


  // Space the floating mini-player and tab bar take at the bottom,
  // so scrolling content can end above them.
  double get bottomInset => 152 + MediaQuery.paddingOf(context).bottom;

  // This method builds the app shell: the selected screen, with the
  // mini-player and tab bar floating over it as glass.
  @override
  Widget build(BuildContext context) {
    final safe = MediaQuery.paddingOf(context);

    // The Song Detector fills the whole screen. Other screens stay below the
    // status bar, and only Home, Library and Search scroll under the bars.
    Widget screen = buildSelectedScreen();
    if (selectedTab != 5) {
      final scrollsUnderBars = selectedTab <= 2 && !showingFavorites;
      screen = SafeArea(
        bottom: false,
        child: Padding(
          padding: EdgeInsets.only(bottom: scrollsUnderBars ? 0 : bottomInset),
          child: screen,
        ),
      );
    }

    return Scaffold(
      backgroundColor: background,
      body: Stack(
        children: [
          // MAIN SCREEN changes based on the selected tab.
          // Screens fade and rise slightly when switching.
          Positioned.fill(
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 320),
              switchInCurve: ease,
              switchOutCurve: ease,
              layoutBuilder: (current, previous) => Stack(
                fit: StackFit.expand,
                children: [...previous, ?current],
              ),
              transitionBuilder: (child, animation) => FadeTransition(
                opacity: animation,
                child: SlideTransition(
                  position: Tween(
                    begin: const Offset(0, 0.015),
                    end: Offset.zero,
                  ).animate(animation),
                  child: child,
                ),
              ),
              child: KeyedSubtree(
                key: ValueKey('$selectedTab-$showingFavorites'),
                child: screen,
              ),
            ),
          ),

          // Back button on the Song Detector and Lyric Search.
          if (selectedTab >= 4)
            Positioned(
              top: safe.top + 8,
              left: 16,
              child: Glass(
                radius: 24,
                child: IconButton(
                  onPressed: goBack,
                  tooltip: 'Back',
                  icon: const Icon(
                    CupertinoIcons.chevron_back,
                    size: 20,
                    color: Colors.white,
                  ),
                ),
              ),
            ),

          // MINI-PLAYER and TAB BAR, floating above the screen.
          Positioned(
            left: 16,
            right: 16,
            bottom: safe.bottom > 20 ? safe.bottom - 8 : 12,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                buildMiniPlayer(),
                const SizedBox(height: 8),
                buildTabBar(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // MINI-PLAYER
  // Displays the current song and playback controls.
  Widget buildMiniPlayer() {
    return Glass(
      radius: 28,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(8, 4, 4, 4),
        child: Row(
          children: [
            // Album cover from iTunes (a music note until it loads).
            ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: SizedBox.square(
                dimension: 40,
                child: Cover(url: currentArtwork, iconSize: 18),
              ),
            ),

            const SizedBox(width: 12),

            // Displays the song title and artist.
            Expanded(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    currentSong,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w600,
                    ),
                  ),

                  // Live bars before the artist while audio plays.
                  Row(
                    children: [
                      if (isPlaying) ...[
                        const LiveBars(height: 10),
                        const SizedBox(width: 6),
                      ],
                      Expanded(
                        child: Text(
                          currentArtist,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            color: textSecondary,
                            fontSize: 13,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            // Play or pause button; the icon cross-fades.
            IconButton(
              onPressed: togglePlay,
              tooltip: isPlaying ? 'Pause' : 'Play',
              icon: AnimatedSwitcher(
                duration: const Duration(milliseconds: 160),
                transitionBuilder: (child, animation) => FadeTransition(
                  opacity: animation,
                  child: ScaleTransition(scale: animation, child: child),
                ),
                child: Icon(
                  isPlaying
                      ? CupertinoIcons.pause_fill
                      : CupertinoIcons.play_fill,
                  key: ValueKey(isPlaying),
                  color: Colors.white,
                  size: 22,
                ),
              ),
            ),

            // Next song button.
            IconButton(
              onPressed: nextSong,
              tooltip: 'Next',
              icon: const Icon(
                CupertinoIcons.forward_fill,
                color: Colors.white,
                size: 22,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // TAB BAR
  // Allows users to select different app sections.
  Widget buildTabBar() {
    return Glass(
      radius: 32,
      child: Padding(
        padding: const EdgeInsets.all(4),
        child: Row(
          children: [
            navigationItem(CupertinoIcons.house_fill, 'Home', 0),
            navigationItem(CupertinoIcons.music_albums_fill, 'Library', 1),
            navigationItem(CupertinoIcons.search, 'Search', 2),
            navigationItem(CupertinoIcons.music_note_list, 'Playlist', 3),
          ],
        ),
      ),
    );
  }

  // This reusable function creates an individual genre card.
  // It displayed a coloured background, an artist image and a genre name.
  Widget genreCard(Map<String, dynamic> genre) {
    
    // GestureDetector allows the user to tap the genre cards.
    return GestureDetector(
      
      // When tapped, the selected genre is placed in the search bar.
      onTap: () => selectGenre(genre['name']),

      child: Container(
        
        // Sets the card height using the genre list
        height: genre['height'],

        //makes the card fill the available column width
        width: double.infinity,

        // Sets the cards background colour and rounded corners.
        decoration: BoxDecoration(
          color: genre['color'],
          borderRadius: BorderRadius.circular(5),
        ),

        //keeps the image inside the cards boundaries
        clipBehavior: Clip.antiAlias,

        //stack allows the image and genre name to overlap
        child: Stack(
          children: [

            //positions the artist image across the card
            Positioned.fill(
              child: Transform.scale(
                //Enlarge or reduce each genre image individually
                scale: genre['imageScale'] ?? 1.0,

                alignment:
                  genre['imageAlignment'] ?? Alignment.bottomCenter,
                  
                child: Image.asset( 
                //loads the image using its file path
                genre['image'],

                //fits the image inside the card without cropping it
                fit: BoxFit.contain,

                alignment:
                  genre['imageAlignment'] ?? Alignment.bottomCenter,

                //display a music from icon if the image cannot load
                errorBuilder: (context, error, stackTrace) {
                  return const Center(
                    child: Icon(
                      Icons.music_note,
                      size: 45,
                      color: Colors.black54,
                    ),
                  );
                },
              ),
            ),
          ),
            
            //positions the genre name in the top-left corner
            Positioned(
              top: 7,
              left: 7,
              
              //displays the genre name
              child: Text(
                genre['name'],
                
                //styles the genre name
                style: const TextStyle(
                  color: Colors.black,
                  fontSize: 17,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }


  // This function creates each tab bar item.
  // The selected tab gets a lighter capsule behind it and the accent color.
  Widget navigationItem(
    IconData icon,
    String label,
    int index,
  ) {
    // Checks whether this navigation item is selected.
    final bool selected = selectedTab == index;
    final Color color = selected ? accent : Colors.white;

    return Expanded(
      child: Semantics(
        button: true,
        selected: selected,
        child: GestureDetector(
          behavior: HitTestBehavior.opaque,

          // Updates the selected tab when tapped.
          onTap: () => selectNavigation(index),

          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            curve: ease,
            height: 56,
            decoration: BoxDecoration(
              color: selected
                  ? const Color(0x24FFFFFF)
                  : const Color(0x00FFFFFF),
              borderRadius: BorderRadius.circular(28),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(icon, color: color, size: 22),
                const SizedBox(height: 3),
                Text(
                  label,
                  style: TextStyle(
                    color: color,
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
