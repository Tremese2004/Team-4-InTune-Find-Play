
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
        scaffoldBackgroundColor: const Color(0xFF171323),
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
  final Color background = const Color(0xFF171323);
  final Color purple = const Color(0xFFB69AFF);
  final Color pink = const Color(0xFFEA91D8);
  final Color cardBackground = const Color(0xFF292238);

  // Stores the message displayed after a search.
  String searchMessage = '';

  // Stores the song and artist shown in the mini-player.
  String currentSong = 'Blinding Lights';
  String currentArtist = 'The Weeknd';

  // Tracks whether the mini-player is playing or paused.
  bool isPlaying = false;

  // Keeps track of which bottom navigation tab is selected.
  // 0 = Home, 1 = Library, 2 = Search, 3 = Playlist.
  int selectedTab = 2;

  // This list stores the information for all nine music genres.
  // Each genre has a name, background colour, image, and height.
  final List<Map<String, dynamic>> genres = [
    {
      'name': 'Hip Hop',
      'color': const Color(0xFF55DCE0),
      'image': 'assets/images/hip_hop.png',
      'height': 160.0,
    },
    {
      'name': 'R&B',
      'color': const Color(0xFFFF555B),
      'image': 'assets/images/rnb.png',
      'height': 190.0,
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
      'image': 'assets/images/afro_beats.png',
      'height': 200.0,
    },
    {
      'name': 'Hits',
      'color': const Color(0xFFFF59BB),
      'image': 'assets/images/hits.png',
      'height': 235.0,
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
  void togglePlay() {
    setState(() {
      // Changes the playing status to its opposite.
      isPlaying = !isPlaying;
    });
  }

  // This function changes the song displayed in the mini-player.
  void nextSong() {
    setState(() {
      currentSong = 'Next Song';
      currentArtist = 'Artist Name';

      // The new placeholder song starts in the paused state.
      isPlaying = false;
    });
  }

  // This function updates the selected bottom navigation tab.
  void selectNavigation(int index) {
    setState(() {
      selectedTab = index;
    });

    // Displays a message for screens that have not been built yet.
    if (index != 2) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            '${['Home', 'Library', 'Search', 'Playlist'][index]} screen coming soon!',
          ),
        ),
      );
    }
  }

  // Disposes of the search controller when the screen is removed.
  // This helps prevent unnecessary memory use.
  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  // This method builds everything displayed on the Music Search screen.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: background,

      // SafeArea keeps content away from the phone's status bar
      // and other system areas.
      body: SafeArea(
        child: Column(
          children: [

            // MAIN SCREEN CONTENT
            // Expanded allows this section to use the available space.
            Expanded(
              child: SingleChildScrollView(
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
                            borderRadius: BorderRadius.circular(30),
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

                              //Displays the blues card
                              genreCard(genres[8]),
                            ],
                          ),
                        ),
                      ],
                    ),
            // MINI-PLAYER
            // Displays the current song and playback controls.
            Container(
              color: cardBackground,

              // Adds spacing inside the mini-player.
              padding: const EdgeInsets.symmetric(
                horizontal: 18,
                vertical: 13,
              ),

              child: Row(
                children: [

                  // Placeholder album artwork.
                  Container(
                    height: 65,
                    width: 65,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [purple, pink],
                      ),
                      borderRadius: BorderRadius.circular(16),
                    ),

                    child: const Icon(
                      Icons.music_note,
                      color: Color(0xFF171323),
                      size: 37,
                    ),
                  ),

                  const SizedBox(width: 13),

                  // Displays the song title and artist.
                  Expanded(
                    child: Column(
                      crossAxisAlignment:
                          CrossAxisAlignment.start,
                      children: [
                        Text(
                          currentSong,
                          style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),

                        const SizedBox(height: 4),

                        Text(
                          currentArtist,
                          style: const TextStyle(
                            color: Color(0xFFB8B3C9),
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Play or pause button.
                  IconButton(
                    onPressed: togglePlay,
                    icon: Icon(
                      isPlaying
                          ? Icons.pause
                          : Icons.play_arrow,
                      color: purple,
                      size: 31,
                    ),
                  ),

                  // Next song button.
                  IconButton(
                    onPressed: nextSong,
                    icon: Icon(
                      Icons.skip_next,
                      color: pink,
                      size: 31,
                    ),
                  ),
                ],
              ),
            ),

            // BOTTOM NAVIGATION BAR
            // Allows users to select different app sections.
            Container(
              color: const Color(0xFF211C31),

              padding: const EdgeInsets.symmetric(
                vertical: 9,
                horizontal: 5,
              ),

              child: Row(
                mainAxisAlignment:
                    MainAxisAlignment.spaceAround,
                children: [

                  // Home navigation button.
                  navigationItem(
                    Icons.home_outlined,
                    'Home',
                    0,
                  ),

                  // Library navigation button.
                  navigationItem(
                    Icons.library_music_outlined,
                    'Library',
                    1,
                  ),

                  // Search navigation button.
                  navigationItem(
                    Icons.search,
                    'Search',
                    2,
                  ),

                  // Playlist navigation button.
                  navigationItem(
                    Icons.queue_music,
                    'Playlist',
                    3,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // This reusable function creates an individual genre card.
  // It displayed a coloured background, an artist image and a genre name.

  Widget navigationItem(Map<String, dynamic> genre) {

    // GestureDetector allows the user to tap the genre cards.
    return GestureDetector(

      // When tapped, the selected genre is placed in the search bar.
      onTap: () => selectGenre(genre['name']),

      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [

          // Creates the rounded background behind the selected icon.
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 22,
              vertical: 7,
            ),

            decoration: BoxDecoration(
              // Highlights the selected navigation item.
              color: selected
                  ? const Color(0xFF493B67)
                  : Colors.transparent,

              borderRadius: BorderRadius.circular(30),
            ),

            // Displays the navigation icon.
            child: Icon(
              icon,
              color: selected
                  ? Colors.white
                  : const Color(0xFFB8B3C9),
              size: 27,
            ),
          ),

          const SizedBox(height: 4),

          // Displays the navigation label underneath the icon.
          Text(
            label,
            style: TextStyle(
              color: selected
                  ? Colors.white
                  : const Color(0xFFB8B3C9),
              fontSize: 13,
            ),
          ),
        ],
      ),
    );
  }
}
