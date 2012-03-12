'''
Created on Mar 11, 2012

@author: tharrison
'''
import java.awt.Canvas as Canvas
import java.lang.Runnable as Runnable
import java.lang.Thread as Thread
import java.awt.Graphics as Graphics
import java.awt.image.BufferedImage as BufferedImage
import java.lang.System as System
import java.text.DecimalFormat as DecimalFormat
import java.awt.Dimension as Dimension
import java.awt.Component as Component
import java.awt.Color as Color
import java.lang.InterruptedException as InterruptedException
import java.lang.Exception as JavaException

from src.game.game_time import GameTime
from src.game.game_component import GameComponent

class GameBase(Runnable):
    components = GameComponent
    canvas = Canvas
    thread = Thread
    dbg = Graphics
    db_image = BufferedImage
    
    running = False
    is_paused = False
    game_over = False
    is_applet = False
    size_changed = False
    game_time = GameTime()
    updates = 0
    
    NO_DELAYS_PER_YIELD = 16
    MAX_FRAME_SKIPS = 5
    period = None
    game_start_time = None
    frames_skipped = None
    
    gelapsed_before = System.nanoTime()
    gelapsed_after = System.nanoTime()
    
    MAX_STAT_INTERVAL = 1
    NUM_FPS = 10
    stats_interval = 0
    prev_stats_time = 0
    total_elapsed_time = 0
    time_spend_in_game = 0
    frame_count = 0
    fps_store = []
    stats_count = 0
    average_fps = 0
    total_frames_skipped = 0
    ups_store = 0
    average_ups = 0
    df = DecimalFormat("0.##")


    def set_size(self, size):
        self.canvas.setSize(size)
        self.size_changed = True


    def set_resolution(self, size):
        self.set_size(size)


    def get_resolution(self):
        return Dimension(self.db_image.getWidth(), self.db_image.getHeight())


    def get_is_active(self):
        if self.is_paused == True:
            return False
        else:
            return True


    def get_is_applet(self):
        return self.is_applet


    def set_is_applet(self, flag):
        if type(flag) is not type(True):
            raise Exception("Flag passed to set_is_applet not a boolean. Got %s instead." % type(flag))
        self.is_applet = flag


    def get_stats_avg_fps(self):
        return self.average_fps


    def get_stats_avg_ups(self):
        return self.average_ups


    def __init__(self, size, fps):
        self.set_size(size)
        Component.setPreferredSize(size)
        Component.setMinimumSize(size)
        Component.setMaximumSize(size)
        
        Component.setBackground(Color.white)
        
        Component.setFocusable(True)
        Component.requestFocus()
        
        db_image = BufferedImage(size.width, size.height, BufferedImage.TYPE_INT_RGB)
        
        self.fps_store = self.NUM_FPS
        self.ups_store = self.NUM_FPS
        i = 0
        if i < self.NUM_FPS:
            self.fps_store[i] = 0
            self.ups_store[i] = 0
            i += 1


    def run(self):
        before_time = None
        after_time = None
        time_diff = None
        sleep_time = None
        over_sleep_time = 0
        no_delays = 0
        excess = 0
        
        game_start_time = System.nanoTime()
        prev_stats_time = game_start_time
        before_time = game_start_time
        
        running = True
        
        while running:
            self.game_update()
            self.game_render()
            self.paint_screen()
            
            after_time = System.nanoTime()
            time_diff = after_time - before_time
            sleep_time = (self.period - time_diff) - over_sleep_time
            
            if sleep_time > 0:
                try:
                    Thread.sleep(sleep_time)
                except InterruptedException as e:
                    pass
                over_sleep_time = (System.nanoTime() - after_time) - sleep_time
            else:
                excess -= sleep_time
                over_sleep_time = 0
                
                if (no_delays + 1) >= self.NO_DELAYS_PER_YIELD:
                    Thread.yield()
                    no_delays = 0
            
            before_time = System.nanoTime()
            
            skips = 0
            
            while excess > self.period and skips < self.MAX_FRAME_SKIPS:
                excess -= self.period
                self.game_update()
                skips += 1
            
            self.frames_skipped += skips
            
            self.store_stats()
        
        self.print_stats()
        System.exit(0)


    def store_stats(self):
        self.frame_count += 1
        self.stats_interval += self.period
        
        if self.stats_interval >= self.MAX_STAT_INTERVAL:
            time_now = System.nanoTime()
            self.time_spend_in_game = time_now - self.game_start_time
            
            real_elapsed_time = time_now - self.prev_stats_time
            self.total_elapsed_time += real_elapsed_time
            
            self.total_frames_skipped += self.frames_skipped
            
            if self.total_elapsed_time > 0:
                actual_fps = self.frame_count / self.total_elapsed_time
                actual_ups = (self.frame_count + self.total_frames_skipped) / self.total_elapsed_time
            
            self.fps_store[self.stats_count % self.NUM_FPS] = actual_fps
            self.ups_store[self.stats_count % self.NUM_FPS] = actual_ups
            self.stats_count += 1
            
            i = 0
            if i < self.NUM_FPS:
                total_fps = self.fps_store[i]
                total_ups = self.ups_store[i]
                i += 1
            
            if self.stats_count < self.NUM_FPS:
                self.average_fps = total_fps / self.stats_count
                self.average_ups = total_ups / self.stats_count
            else:
                self.average_fps = total_fps / self.NUM_FPS
                self.average_ups = total_ups / self.NUM_FPS
            
            self.frames_skipped = 0
            self.prev_stats_time = time_now
            self.stats_interval = 0


    def game_update(self):
        self.gelapsed_after = System.nanoTime()
        
        self.game_time.elapsed_game_time.set_span(self.gelapsed_before, self.gelapsed_after)
        self.game_time.elapsed_real_time.set_span(self.gelapsed_before, self.gelapsed_after)
        
        self.game_time.total_game_time.set_span(self.game_start_time, self.gelapsed_after)
        self.game_time.total_real_time.set_span(self.game_start_time, self.gelapsed_after)
        
        self.gelapsed_before = System.nanoTime()
        
        if self.running and self.is_paused is not True and self.game_over is not True:
            for item in self.components.getComponents():
                item.update(self.game_time)
            self.updates += 1


    def get_render(self):
        if self.db_image is None or self.size_changed:
            size = Dimension(Component.getWidth(), Component.getHeight())
            self.set_size(size)
            Component.setPreferredSize(size)
            Component.setMinimumSize(size)
            Component.setMaximumSize(size)
            self.size_changed = False
            
            try:
                self.db_image = BufferedImage(Component.getWidth(), Component.getHeight(), BufferedImage.TYPE_INT_RGB)
            except JavaException as e:
                self.db_image = None
                System.out.println("Render Error: %s" % e)
                System.out.println("Render Error: Buffer not initialized properly")
                System.out.println("Render Error: Resolving...")


    def paint_screen(self):
        bs = Canvas.getBufferStrategy()
        if bs is None:
            Canvas.createBufferStrategy(3)
        
        g = bs.getDrawGraphics()
        g.drawImage(self.db_image, 0, 0, Component.getWidth(), Component.getHeight(), None)
        g.dispose()
        bs.show()


    def start_game(self):
        if self.running:
            return
        self.thread = Thread(self)
        self.thread.start()
        self.running = True


    def stop_game(self):
        if self.running is None:
            return
        self.thread.stop()
        self.running = False


    def set_preferred_fps(self, fps):
        self.period = 1000/fps


    def reset_elapsed_time(self):
        self.game_time.elapsed_game_time.set_span(0)
        self.game_time.elapsed_real_time.set_span(0)


    def add_component(self, game_component):
        game_component.initialize()
        game_component.load_content()
        self.components.add(game_component)


    def remove_component(self, game_component):
        game_component.unload_content()
        self.components.remove(game_component)


    def resume_game(self):
        self.is_paused = False


    def pause_game(self):
        self.is_paused = True


    def print_stats(self):
        System.out.println("Frame Count/Loss: %s / %s" % (self.frame_count, self.total_frames_skipped))
        System.out.println("Average FPS: %s" % self.df.format(self.average_fps))
        System.out.println("Average UPS: %s" % self.df.format(self.average_ups))
        System.out.println("TIme Spend: %s secs" % self.time_spend_in_game)
        System.out.println("Total Updates: %s" % self.updates)
        System.out.println("dbImage: %s" % self.db_image.toString())