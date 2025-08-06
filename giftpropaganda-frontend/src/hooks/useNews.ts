import { useState, useEffect, useCallback } from 'react';
import { NewsItem } from '../types';
import { fetchNews } from '../api/news';

export const useNews = (category: string = 'all') => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [initialized, setInitialized] = useState(false);

  const getNews = useCallback(async (isLoadMore: boolean = false) => {
    try {
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Request timeout')), 8000)
      );
      
      const fetchPromise = fetchNews(
        category === 'all' ? undefined : category, 
        page, 
        20
      );
      
      const response = await Promise.race([fetchPromise, timeoutPromise]) as any;

      if (response && response.data) {
        if (isLoadMore) {
          setNews(prev => [...prev, ...response.data]);
        } else {
          setNews(response.data);
        }
        setHasMore(response.data.length === 20);
      }
    } catch (error) {
      console.error('Ошибка загрузки новостей:', error);
      setError('Не удалось загрузить новости');
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, [category, page]);

  const loadMore = async () => {
    if (!loadingMore && hasMore) {
      const nextPage = page + 1;
      setPage(nextPage);
      
      try {
        setLoadingMore(true);
        const response = await fetchNews(
          category === 'all' ? undefined : category,
          nextPage,
          20,
          false
        );
        
        setNews(prev => [...prev, ...response.data]);
        setHasMore(response.data.length === 20 && (response.total || 0) > nextPage * 20);
        

      } catch (err) {
        console.error('Ошибка при загрузке дополнительных новостей:', err);
        setPage(prev => prev - 1);
      } finally {
        setLoadingMore(false);
      }
    }
  };

  const initializeNews = useCallback(async () => {
    if (!initialized) {
      setLoading(true);
      setPage(1);
      setHasMore(true);
      await getNews();
      setInitialized(true);
    }
  }, [initialized, getNews]);

  useEffect(() => {
    if (category !== 'all') {
      setPage(1);
      setHasMore(true);
      setNews([]);
      setInitialized(false);
      getNews();
    }
  }, [category, getNews]);

  return {
    news,
    loading,
    error,
    hasMore,
    loadingMore,
    loadMore,
    initializeNews
  };
}; 