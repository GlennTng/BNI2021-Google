"""A video player class."""

import random
import re

from .video import Video
from .video_library import VideoLibrary
from .video_playlist import Playlist

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        # shows the status of whether a video is playing
        self.play_status = False
        # shows the current video that is playing
        self.current_video = []
        # shows if current video is paused
        self.paused = False
        # dictionary to store playlist
        self.playlist_dict = {}
        # list of all the videos
        self.video_list = self._video_library.get_all_videos()
        # dict of all the songs are their flags
        self.video_flag = {}
        for video in self.video_list:
            self.video_flag[video] = ""

    def number_of_videos(self):
        num_videos = len(self.video_list)
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        video_list = []
        print("Here's a list of all available videos:")
        for video in self._video_library.get_all_videos():
            title = Video.title.__get__(video)
            id = Video.video_id.__get__(video)
            tags = Video.tags.__get__(video)
            if self.video_flag[video]:
                video_list.append(title + " (" + id + ") " + "[" + (" ".join(tag for tag in tags)) + "]" + " - FLAGGED (reason: " + self.video_flag[video] + ")")
            else:
                video_list.append( title + " (" + id + ") " + "[" + (" ".join(tag for tag in tags)) + "]")
        video_list.sort()
        for vid in video_list:
            print(vid)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        videos = self._video_library.get_all_videos()
        if not video_id:
            print("No videos available")
        else:
            for video in videos:
                if video._video_id == video_id:
                    if self.video_flag[video]:
                        print("Cannot play video: Video is currently flagged (reason:", self.video_flag[video] +")")
                        return
                    else:
                        if self.play_status:
                            print("Stopping video:", self.current_video[0])
                        print("Playing video:", video._title)
                        self.current_video = [video._title, video._video_id, video._tags]
                        self.play_status = True
                        self.paused = False
                        return
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self.play_status:
            self.play_status = False
            print("Stopping video:", self.current_video[0])
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        choices = []
        for video in self.video_flag:
            if not self.video_flag[video]:
                choices.append(video)
        try:
            random_video = (random.randint(0, len(choices) - 1))
            choice = choices[random_video]
        except:
            random_video = 0
            choice = ""
        self.play_video(choice)

    def pause_video(self):
        """Pauses the current video."""
        if not self.play_status:
            print("Cannot pause video: No video is currently playing")
        else:
            if not self.paused:
                self.paused = True
                print("Pausing video:", self.current_video[0])
            else:
                print("Video already paused:", self.current_video[0])

    def continue_video(self):
        """Resumes playing the current video."""
        if not self.play_status:
            print("Cannot continue video: No video is currently playing")
        else:
            if self.paused:
                self.paused = False
                print("Continuing video:", self.current_video[0])
            else:
                print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if not self.play_status:
            print("No video is currently playing")
        else:
            message = "Currently playing: " + self.current_video[0] + " (" + self.current_video[1] + ") " + "[" + (" ".join(tag for tag in self.current_video[2])) + "]"
            if not self.paused:
                print(message)
            else:
                print(message, "- PAUSED")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in (name.lower() for name in self.playlist_dict.keys()):
            pl = Playlist(playlist_name)
            self.playlist_dict[playlist_name] = pl
            print("Successfully created new playlist:", pl._name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower() for name in self.playlist_dict.keys()):
            print("Cannot add video to", playlist_name + ":", "Playlist does not exist")
        else:
            video = self._video_library.get_video(video_id)
            if self.video_flag[video]:
                print("Cannot add video to", playlist_name_old + ":", "Video is currently flagged (reason:", self.video_flag[video] + ")")
                return
            for key in self.playlist_dict.keys():
                if key.lower() == playlist_name.lower():
                    playlist_name = key
            video_list = self.playlist_dict[playlist_name]._videos
            try:
                video_name = self._video_library.get_video(video_id)._title
            except:
                video_name = ""
            if not video_name:
                print("Cannot add video to", playlist_name_old + ":", "Video does not exist")
            elif video_id in video_list:
                print("Cannot add video to", playlist_name + ":", "Video already added")
            else:
                video_list.append(video_id)
                obj = self.playlist_dict[playlist_name]
                obj.x(video_list)
                self.playlist_dict[playlist_name] = obj
                print("Added video to", playlist_name_old + ":", video_name)
        
    def show_all_playlists(self):
        """Display all playlists."""
        if not self.playlist_dict:
            print("No playlists exist yet")
        else:
            name_list = []
            print("Showing all playlists:")
            for key in self.playlist_dict.keys():
                name_list.append(key)
            sorted_names = sorted(name_list, key=str.casefold)
            for name in sorted_names:
                print(name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower() for name in self.playlist_dict.keys()):
            print("Cannot show playlist", playlist_name + ":", "Playlist does not exist")
        else:
            for key in self.playlist_dict.keys():
                if key.lower() == playlist_name.lower():
                    playlist_name = key
            obj = self.playlist_dict[playlist_name]
            video_list = obj._videos
            print("Showing playlist:", playlist_name_old)
            if video_list:
                for video_id in video_list:
                    title = self._video_library.get_video(video_id)._title
                    id = self._video_library.get_video(video_id)._video_id
                    tags = self._video_library.get_video(video_id)._tags
                    video =  self._video_library.get_video(id)
                    if self.video_flag[video]:
                        print(video._title + " (" + video._video_id + ") " + "[" + (" ".join(video._tags)) + "]", "- FLAGGED (reason:", self.video_flag[video] +")")
                    else:
                        print(title + " (" + id + ") " + "[" + (" ".join(tag for tag in tags)) + "]")
            else:
                print("No videos here yet")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower() for name in self.playlist_dict.keys()):
            print("Cannot remove video from", playlist_name + ":", "Playlist does not exist")
        else:
            for key in self.playlist_dict.keys():
                if key.lower() == playlist_name.lower():
                    playlist_name = key
            obj = self.playlist_dict[playlist_name]
            video_list = obj._videos
            try:
                video_name = self._video_library.get_video(video_id)._title
            except:
                video_name = ""
            if video_id in video_list:
                video_list.remove(video_id)
                obj.x(video_list)
                print("Removed video from", playlist_name_old + ":", video_name)
            else:
                if not video_name:
                    print("Cannot remove video from", playlist_name_old + ":", "Video does not exist")
                else:
                    print("Cannot remove video from", playlist_name_old + ":", "Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower() for name in self.playlist_dict.keys()):
            print("Cannot clear playlist", playlist_name + ":", "Playlist does not exist")
        else:
            for key in self.playlist_dict.keys():
                if key.lower() == playlist_name.lower():
                    playlist_name = key
            obj = self.playlist_dict[playlist_name]
            video_list = obj._videos
            video_list.clear()
            obj.x(video_list)
            print("Successfully removed all videos from", playlist_name_old)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower() for name in self.playlist_dict.keys()):
            print("Cannot delete playlist", playlist_name + ":", "Playlist does not exist")
        else:
            for key in self.playlist_dict.keys():
                if key.lower() == playlist_name.lower():
                    playlist_name = key
            obj = self.playlist_dict[playlist_name]
            del obj
            self.playlist_dict.pop(playlist_name, None)
            print("Deleted playlist:", playlist_name_old)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = []
        for video in self.video_list:
            video_details = []
            title = video._title
            id = "(" + video._video_id + ")"
            tags = "[" + (" ".join(tag for tag in video._tags)) + "]"
            video_details.append(str(title))
            video_details.append(id)
            video_details.append(tags)
            videos.append(video_details)
        r = re.compile("(?i)" + search_term)
        newlist = list(filter(r.findall, (list[0] for list in videos)))
        if newlist:
            newlist = sorted(newlist, key=str.casefold)
            print("Here are the results for", search_term + ":")
            found_list = []
            id_list = []
            for detail_list in videos:
                if detail_list[0] in newlist:
                    video = self._video_library.get_video(detail_list[1][1:-1])
                    if self.video_flag[video]:
                        continue
                    else:
                        id_list.append(detail_list[1])
                        found_list.append(detail_list[0] + " " + detail_list[1] + " " + detail_list[2])
            for i in range(len(found_list)):
                print(f"{i+1}) {found_list[i]}")
            print("Would you like to play any of the above? If yes, specify the number of the video.\nIf your answer is not a valid number, we will assume it's a no.")
            reply = input()
            try:
                if int(reply) <= 0 or int(reply) > len(newlist):
                    return
                else:
                    self.play_video(id_list[int(reply) - 1][1:-1])
            except:
                return
        else:
            print("No search results for", search_term)
                
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = []
        for video in self.video_list:
            video_details = []
            title = video._title
            id = "(" + video._video_id + ")"
            tags = "[" + (" ".join(tag for tag in video._tags)) + "]"
            video_details.append(str(title))
            video_details.append(id)
            video_details.append(tags)
            videos.append(video_details)
        if not video_tag.startswith("#"):
            print("No search results for", video_tag)
        else:
            r = re.compile("(?i)" + video_tag)
            newlist = list(filter(r.findall, (list[2] for list in videos)))
            if not newlist:
                print("No search results for", video_tag)
            else:
                print("Here are the results for", video_tag + ":")
                found_list = []
                id_list = []
                for detail_list in videos:
                    if detail_list[2] in newlist:
                        video = self._video_library.get_video(detail_list[1][1:-1])
                        if self.video_flag[video]:
                            continue
                        else:
                            found_list.append(detail_list[0] + " " + detail_list[1] + " " + detail_list[2])
                            id_list.append(detail_list[1])
                found_list = sorted(found_list, key=str.casefold)
                for i in range(len(found_list)):
                    print(f"{i+1}) {found_list[i]}")
                print("Would you like to play any of the above? If yes, specify the number of the video.\nIf your answer is not a valid number, we will assume it's a no.")
                reply = input()
                try:
                    if int(reply) <= 0 or int(reply) > len(found_list):
                        return
                    else:
                        self.play_video(id_list[int(reply) - 1][1:-1])
                except:
                    return
                
                
    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video:
            if not self.video_flag[video]:
                self.video_flag[video] = flag_reason
                if flag_reason:
                    if self.play_status:
                        if self.video_flag[self._video_library.get_video(self.current_video[1])]:
                            print("Stopping video:", self.current_video[0])
                            self.play_status = False
                            self.current_video = ""
                    print("Successfully flagged video:", video._title, "(reason:", flag_reason +")")
                else:
                    self.video_flag[video] = "Not supplied"
                    print("Successfully flagged video:", video._title, "(reason: Not supplied)")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video:
            if self.video_flag[video]:
                self.video_flag[video] = ""
                print("Successfully removed flag from video:", video._title)
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")

