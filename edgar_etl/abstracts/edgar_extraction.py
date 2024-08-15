from abc import ABC, abstractmethod


class EdgarExtraction(ABC):

    def extract(self, cik_list, from_date, to_date, request_delay_sec=0, extraction_type="delegate", use_cache=True,
                cache_max_days=1):
        if extraction_type == "xbrl" or extraction_type is None:
            return self._xbrl_extraction(cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days)
        elif extraction_type == "gen_ai":
            return self._gen_ai_extraction(cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days)
        elif extraction_type == "delegate":
            return self._delegate_extraction(cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days)
        else:
            return None

    @abstractmethod
    def _xbrl_extraction(self, cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days):
        pass

    @abstractmethod
    def _gen_ai_extraction(self, cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days):
        pass

    @abstractmethod
    def _delegate_extraction(self, cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days):
        pass
