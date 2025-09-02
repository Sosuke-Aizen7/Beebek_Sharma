import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { AxiosResponse, AxiosError } from 'axios';

// Generic hook for API calls with loading and error states
export const useApiCall = <T>(
  apiCall: () => Promise<AxiosResponse<T>>,
  dependencies: any[] = []
) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiCall();
        setData(response.data);
      } catch (err) {
        const axiosError = err as AxiosError;
        setError(axiosError.message || 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, dependencies);

  return { data, loading, error, refetch: () => fetchData() };
};

// Hook for mutations with optimistic updates
export const useMutationWithToast = <TData, TVariables>(
  mutationFn: (variables: TVariables) => Promise<AxiosResponse<TData>>,
  options?: {
    onSuccess?: (data: TData, variables: TVariables) => void;
    onError?: (error: AxiosError, variables: TVariables) => void;
    invalidateQueries?: string[];
  }
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (variables: TVariables) => {
      const response = await mutationFn(variables);
      return response.data;
    },
    onSuccess: (data, variables) => {
      if (options?.onSuccess) {
        options.onSuccess(data, variables);
      }
      if (options?.invalidateQueries) {
        options.invalidateQueries.forEach((queryKey) => {
          queryClient.invalidateQueries({ queryKey: [queryKey] });
        });
      }
    },
    onError: (error: AxiosError, variables) => {
      if (options?.onError) {
        options.onError(error, variables);
      }
    },
  });
};

// Pagination hook
export const usePagination = (initialPage = 1) => {
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [pageSize] = useState(20);

  const goToPage = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const nextPage = () => goToPage(currentPage + 1);
  const prevPage = () => goToPage(Math.max(1, currentPage - 1));

  return {
    currentPage,
    pageSize,
    goToPage,
    nextPage,
    prevPage,
  };
};

// Debounced search hook
export const useDebounce = <T>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

// Local storage hook
export const useLocalStorage = <T>(key: string, initialValue: T) => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  };

  return [storedValue, setValue] as const;
};