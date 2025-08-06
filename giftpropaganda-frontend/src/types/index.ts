export interface NewsItem {
  id: string | number;
  title: string;
  content?: string;
  text?: string;
  content_html?: string;
  link?: string;
  publish_date?: string;
  date?: string;
  category: string;
  source?: string;
  channel?: string;
  reading_time?: number;
  views_count?: number;
  author?: string;
  subtitle?: string;
  background_image?: string;
  background_color?: string;
  icon?: string;
  gradient_start?: string;
  gradient_end?: string;
  media?: MediaItem[];
}

export interface MediaItem {
  type: 'photo' | 'video';
  url: string;
  thumbnail?: string;
  width?: number;
  height?: number;
}

export interface Category {
  id: string;
  name: string;
  icon: string;
}

export interface APIStatus {
  apiHealth: {
    local: boolean;
    prod: boolean;
  };
} 